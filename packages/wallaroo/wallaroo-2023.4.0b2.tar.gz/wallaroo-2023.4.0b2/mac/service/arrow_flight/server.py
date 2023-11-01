"""This module features the ArrowFlightServer class, that
implements a flight.FlightServerBase that runs inferences
on an Inference object."""

import logging
import threading
from typing import Dict, Generator, List, Set, Tuple

import numpy.typing as npt
import pyarrow as pa
import pyarrow.flight as flight

from mac.config.service import ServerConfig
from mac.exceptions import ArrowRecordBatchConversionError
from mac.inference import Inference
from mac.types import (
    ArrowToNDArrayConverter,
    InferenceData,
    IOArrowDType,
    NDArrayToArrowConverter,
)
from mac.utils.helpers import (
    convert_multi_dim_chunked_array_to_numpy_array,
    convert_numpy_array_to_fixed_shape_tensor_array,
    convert_numpy_array_to_nested_list_array,
    convert_numpy_array_to_pa_array,
    get_io_arrow_dtype_from_column,
    is_numpy_array_multi_dim,
    log_error,
)

logger = logging.getLogger(__name__)

ARROW_TO_ND_ARRAY_CONVERTERS: Dict[IOArrowDType, ArrowToNDArrayConverter] = {
    IOArrowDType.LIST: convert_multi_dim_chunked_array_to_numpy_array,
    IOArrowDType.FIXED_SHAPE_TENSOR: convert_multi_dim_chunked_array_to_numpy_array,
    IOArrowDType.SCALAR: lambda array: array.to_numpy().astype(
        array.type.to_pandas_dtype()
    ),
}

ND_ARRAY_TO_ARROW_CONVERTERS: Dict[IOArrowDType, NDArrayToArrowConverter] = {
    IOArrowDType.LIST: convert_numpy_array_to_nested_list_array,
    IOArrowDType.FIXED_SHAPE_TENSOR: convert_numpy_array_to_fixed_shape_tensor_array,
    IOArrowDType.SCALAR: convert_numpy_array_to_pa_array,
}


class ArrowFlightServer(flight.FlightServerBase):
    """This class implements the Arrow Flight server, that can be used to
    serve an Inference via the Arrow Flight RPC protocol.

    Attributes:
    - inference: An Inference object to serve.
    - server_config: A ServerConfig object.
    - lock: A threading.Lock object.
    - location: A string representing the location of the server.
    """

    def __init__(self, inference: Inference, server_config: ServerConfig):
        self._inference = inference
        self._server_config = server_config
        self._lock = threading.Lock()
        super().__init__(location=self.location)

    @property
    def location(self):
        """This property returns the location of the server."""
        return f"grpc://{self._server_config.host}:{self._server_config.port}"

    def do_action(
        self, context: flight.ServerCallContext, action: flight.Action
    ) -> Generator[flight.Result, None, None]:
        """This method implements the `do_action` method of the FlightServerBase,
        that provides a health check endpoint for the server.

        :param context: A ServerCallContext object.
        :param action: A FlightAction object.

        :return: A Generator of FlightResult objects.

        :raises KeyError: If the action type is not `ping`.
        """
        if action.type == "ping":
            yield flight.Result(pa.py_buffer(b"\n"))
        else:
            raise KeyError(f"Unknown action `{action.type}`.")

    def do_exchange(
        self,
        context: flight.ServerCallContext,
        descriptor: flight.FlightDescriptor,
        reader: flight.FlightStreamReader,
        writer: flight.FlightStreamWriter,
    ) -> None:
        """This method implements the `do_exchange` method of the FlightServerBase
        class.

        :param context: A ServerCallContext object.
        :param descriptor: A FlightDescriptor object.
        :param reader: A FlightStreamReader object.
        :param writer: A FlightStreamWriter object.
        """
        is_first_batch = True
        while True:
            logger.info("Processing data...")
            (
                writer,
                reader,
                is_first_batch,
            ) = self._run_inference_and_write_to_stream(
                writer, reader, is_first_batch
            )
            logger.info("Output data ready to be consumed.")

    def _run_inference_and_write_to_stream(
        self,
        writer: flight.FlightStreamWriter,
        reader: flight.FlightStreamReader,
        is_first_batch: bool,
    ) -> Tuple[flight.FlightStreamWriter, flight.FlightStreamReader, bool]:
        logger.debug("Starting batch processing...")
        for batch in reader.read_chunk():
            if batch is None:
                break
            writer, is_first_batch = self._process_batch(  # type: ignore[no-redef]
                batch, writer, is_first_batch
            )
        logger.debug("Batch processing finished.")

        writer.close()

        return (writer, reader, is_first_batch)

    def _process_batch(
        self,
        batch: pa.RecordBatch,
        writer: flight.MetadataRecordBatchWriter,
        is_first_batch: bool,
    ) -> Tuple[flight.FlightStreamWriter, bool]:
        result = self._run_inference_for_batch(batch)
        return self._write_result(writer, result, is_first_batch)  # type: ignore

    def _run_inference_for_batch(
        self, batch: pa.RecordBatch
    ) -> List[pa.RecordBatch]:
        logger.info("Converting pa.RecordBatch to InferenceData...")
        (
            inference_data,
            io_arrow_dtypes,
        ) = self._convert_record_batch_to_inference_data(batch)

        logger.info("Parsing InferenceData to Inference...")
        self._lock.acquire()
        inference_data = self._inference.predict(  # type: ignore
            input_data=inference_data
        )
        self._lock.release()

        logger.info("Converting InferenceData to pa.RecordBatch...")
        return self._convert_inference_data_to_table_batches(
            inference_data, io_arrow_dtypes
        )

    @log_error(
        ArrowRecordBatchConversionError,
        "Failed to convert pa.RecordBatch to InferenceData.",
    )
    def _convert_record_batch_to_inference_data(
        self,
        batch: pa.RecordBatch,
    ) -> Tuple[InferenceData, Set[IOArrowDType]]:
        table = pa.Table.from_batches([batch])
        inference_data: InferenceData = {}
        io_arrow_dtypes: Set[IOArrowDType] = set()

        for column, column_name in zip(table, table.column_names):
            (
                inference_data[column_name],
                io_arrow_dtype,
            ) = self._convert_column_to_numpy_array(column)
            io_arrow_dtypes.add(io_arrow_dtype)

        io_arrow_dtypes = self._drop_fixed_shape_tensor_dtype_if_multiple_arrow_list_dtypes_found(  # noqa: E501
            io_arrow_dtypes
        )

        return inference_data, io_arrow_dtypes

    def _convert_column_to_numpy_array(
        self,
        column: pa.ChunkedArray,
    ) -> Tuple[npt.NDArray, IOArrowDType]:
        io_arrow_dtype: IOArrowDType = get_io_arrow_dtype_from_column(
            column_type=column.type
        )
        output = ARROW_TO_ND_ARRAY_CONVERTERS[io_arrow_dtype](column)

        return output, io_arrow_dtype

    @staticmethod
    def _drop_fixed_shape_tensor_dtype_if_multiple_arrow_list_dtypes_found(
        io_arrow_dtypes: Set[IOArrowDType],
    ) -> Set[IOArrowDType]:
        if ArrowFlightServer._both_arrow_list_dtypes_found(io_arrow_dtypes):
            message = (
                "Both `IOArrowDType.LIST` and `IOArrowDType.FIXED_SHAPE_TENSOR` "
                "found in incoming data. Sending output data only as "
                "`IOArrowDType.LIST`, if needed..."
            )
            logger.warning(message)

        io_arrow_dtypes.discard(IOArrowDType.FIXED_SHAPE_TENSOR)
        return io_arrow_dtypes

    @staticmethod
    def _both_arrow_list_dtypes_found(
        io_arrow_dtypes: Set[IOArrowDType],
    ) -> bool:
        return {IOArrowDType.LIST, IOArrowDType.FIXED_SHAPE_TENSOR}.issubset(
            io_arrow_dtypes
        )

    @log_error(
        ArrowRecordBatchConversionError,
        "Failed to convert InferenceData to pa.RecordBatch.",
    )
    def _convert_inference_data_to_table_batches(
        self,
        inference_data: InferenceData,
        io_arrow_dtypes: Set[IOArrowDType],
    ) -> List[pa.RecordBatch]:
        data: List[pa.Array] = []
        data_info: List[Tuple[str, pa.DataType]] = []

        for key, value in inference_data.items():
            if is_numpy_array_multi_dim(value):
                io_arrow_dtype = self._get_output_arrow_list_dtype(
                    io_arrow_dtypes
                )
            else:
                io_arrow_dtype = IOArrowDType.SCALAR

            pa_type, pa_array = ND_ARRAY_TO_ARROW_CONVERTERS[io_arrow_dtype](
                value
            )
            data.append(pa_array)
            data_info.append((key, pa_type))
            del pa_array

        return pa.Table.from_arrays(
            data, schema=pa.schema(data_info)
        ).to_batches()

    @staticmethod
    def _get_output_arrow_list_dtype(
        io_arrow_dtypes: Set[IOArrowDType],
    ) -> IOArrowDType:
        try:
            return [
                dtype
                for dtype in io_arrow_dtypes
                if dtype != IOArrowDType.SCALAR
            ][0]
        except (
            IndexError
        ):  # if no matching input type found, return a nested list
            return IOArrowDType.LIST

    def _write_result(
        self,
        writer: flight.FlightStreamWriter,
        result: List[pa.RecordBatch],
        is_first_batch: bool,
    ) -> Tuple[flight.FlightStreamWriter, bool]:
        if is_first_batch is True:
            is_first_batch = False
            logger.debug("Writing schema to stream...")
            writer.begin(result[0].schema)

        for batch in result:
            writer.write_batch(batch)

        return (writer, is_first_batch)
