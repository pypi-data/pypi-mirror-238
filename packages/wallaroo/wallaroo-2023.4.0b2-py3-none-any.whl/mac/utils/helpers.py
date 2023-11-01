"""This module features helper functions for the mac package."""

import functools
import importlib
import inspect
import logging
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Set, Tuple, Type, Union

import numpy as np
import numpy.typing as npt
import pandas as pd
import pyarrow as pa

from mac.exceptions import (
    DirectoryNotExistError,
    FileFormatError,
    PathNotExistError,
)
from mac.inference.creation.inference_builder import InferenceBuilder
from mac.types import ArrowListDType, IOArrowDType

logger = logging.getLogger(__name__)


def convert_dataframe_to_dict_of_numpy_arrays(
    data: pd.DataFrame,
) -> Dict[str, npt.NDArray]:
    """Converts a Pandas DataFrame to a dict of numpy arrays.

    :param data: The data to convert.
    :raises ValueError: If the conversion fails.

    :return: The data converted to a dict of numpy arrays.
    """
    output = {}
    for col in data.columns:
        try:
            output[col] = np.array(data[col].tolist())
        except ValueError:
            message = (
                f"Could not convert column `{col}` to numpy array, due to ValueError. "
                "Converting to numpy array of lists instead."
            )
            logger.debug(message, exc_info=True)
            output[col] = np.array(data[col].tolist(), dtype=object)
    return output


def convert_dataframe_to_numpy(data: pd.DataFrame) -> npt.NDArray:
    """Converts a Pandas DataFrame to a numpy array.

    :param data: The data to convert.

    :return: The data converted to a numpy array.
    """
    return data.to_numpy()


def convert_dict_of_arrays_to_list_of_arrays(
    data: Dict[str, Iterable]
) -> List[Iterable]:
    """Converts a dict of arrays to a list of arrays preserving
    the key order.

    Example:

    {
        "output_1": np.array([1, 2, 3]),
        "output_2": np.array([4, 5, 6]),
    }

    converts to:
    [np.array([1, 2, 3]), np.array([4, 5, 6])]

    :param data: The data to convert.

    :return: The converted data.
    """
    return [data[key] for key in data]


def convert_list_of_arrays_to_dict_of_arrays(
    data: List[Iterable], expected_skeleton: str
) -> Dict[str, Iterable]:
    """Converts a list of arrays to a dict of arrays with sorted
    keys in ascending order.

    Example:
    {
        "output_1": np.array([1, 2, 3]),
        "output_2": np.array([4, 5, 6]),
    }

    :param data: The data to convert.
    :param expected_skeleton: The expected skeleton of the keys.

    :return: The converted data to a dict of iterables.
    """
    return {f"{expected_skeleton}_{i+1}": data for i, data in enumerate(data)}


def convert_list_of_dicts_to_dict_of_numpy_arrays(
    data: List[Dict[str, Any]], expected_keys: List[str]
) -> Dict[str, npt.NDArray]:
    """Converts a list of dicts to a dict of numpy arrays.

    :param data: The data to convert.
    :param expected_keys: The expected keys of the dicts.

    :return: The converted data to a dict of numpy arrays.
    """
    return {
        key: np.array([item[key] for item in data]) for key in expected_keys
    }


def convert_multi_dim_chunked_array_to_numpy_array(
    array: pa.ChunkedArray,
) -> npt.NDArray:
    """Converts a PyArrow chunked array to a numpy array.

    :param array: The PyArrow ChunkedArray to convert.

    :return: The converted data to a numpy array.
    """
    shape = get_shape_of_multi_dim_chunked_array(
        array=array,
        arrow_list_dtype=get_arrow_list_dtype_from_pa_dtype(array.type),
    )

    arrays = [
        row
        for chunk in array.chunks
        for row in flat_values(chunk)
        .to_numpy(zero_copy_only=False)
        .reshape([len(chunk), *shape])
    ]

    return np.array(arrays)


def convert_multi_dim_numpy_array_to_list(data: npt.NDArray) -> List:
    """Converts a multi-dimensional numpy array to a list."""
    if isinstance(data, np.ndarray) and is_numpy_array_multi_dim(data):
        return [
            convert_multi_dim_numpy_array_to_list(element) for element in data
        ]
    return data.tolist() if isinstance(data, np.ndarray) else data


def convert_numpy_array_to_fixed_shape_tensor_array(
    data: npt.NDArray,
) -> Tuple[pa.FixedShapeTensorType, pa.ExtensionArray]:
    """Converts a numpy array to a fixed shape tensor array.

    :param data: The data to convert.

    :return: The converted data to a FixedShapeTensor array,
        along with the PyArrow data type.
    """
    data_type = pa.from_numpy_dtype(data.dtype)
    data_shape = data[0].shape
    tensor_type = pa.fixed_shape_tensor(
        data_type,
        data_shape,
    )
    flattened_array = [item.flatten().tolist() for item in data]

    storage = pa.array(
        flattened_array,
        pa.list_(data_type, len(flattened_array[0])),
    )
    tensor_array = pa.ExtensionArray.from_storage(tensor_type, storage)

    return (tensor_type, tensor_array)


def convert_numpy_array_to_nested_list_array(
    data: npt.NDArray,
) -> Tuple[pa.ListType, pa.ListArray]:
    """Converts a numpy array to a nested list array.

    :param data: The data to convert.

    :return: The converted data to a nested list array,
        along with the PyArrow data type.
    """
    try:
        data_type = pa.from_numpy_dtype(data.dtype)
    except pa.ArrowNotImplementedError:
        item_dtype = get_data_type_of_nested_list(data)
        data_type = (
            pa.null()
            if item_dtype == type(None)
            else pa.from_numpy_dtype(item_dtype)
        )

    max_dim = get_max_depth_of_nested_list(data)
    nested_array = pa.array(
        convert_multi_dim_numpy_array_to_list(data),
        type=nested_pa_list_type_constructor(
            max_dim=max_dim, data_type=data_type
        ),
    )

    return (nested_array.type, nested_array)


def convert_numpy_array_to_pa_array(
    data: npt.NDArray,
) -> Tuple[pa.ListType, pa.Array]:
    """Converts a numpy array to a pa.Array.

    :param data: The data to convert.

    :return: The converted data to a pa.Array,
        along with the PyArrow data type.
    """
    return pa.from_numpy_dtype(data.dtype), pa.array(data)


def flat_values(array: pa.ChunkedArray) -> pa.Array:
    """
    Recursively unnest the `array` until a non-list type is found.

    :param array: The PyArrow ChunkedArray to flatten.

    :return: The inner non-nested values array.
    """
    if isinstance(array, pa.FixedShapeTensorArray):
        array = array.storage
    while pa_type_is_list(array.type):
        array = array.values
    return array


def get_data_type_from_value_type(value_type: pa.DataType) -> pa.DataType:
    """Gets the data type from the given value type.

    :param value_type: The value type to get the data type from.

    :return: The PyArrow data type.
    """
    try:
        return get_data_type_from_value_type(value_type.value_type)
    except AttributeError:
        return value_type


def get_data_type_of_nested_list(data: Union[npt.NDArray, List]) -> Type:
    """Gets the data type of a nested list.

    :param data: The nested list to get the data type of.

    :return: The data type of the nested list.
    """
    if isinstance(data, (np.ndarray, list)):
        return get_data_type_of_nested_list(data[0])
    return type(data)


def get_io_arrow_dtype_from_column(
    column_type: pa.DataType,
) -> IOArrowDType:
    """Gets the IOArrowDType from the given column.

    :param column: The column to get the IOArrowDType from.
    """
    if pa_type_is_fixed_shape_tensor(column_type):
        return IOArrowDType.FIXED_SHAPE_TENSOR
    elif pa_type_is_list(column_type):
        return IOArrowDType.LIST
    else:
        return IOArrowDType.SCALAR


def get_arrow_list_dtype_from_pa_dtype(
    pa_type: pa.DataType,
) -> ArrowListDType:
    """Gets the ArrowListDType from a given pa.DataType.

    :param pa_type: The pa.DataType to convert.

    :return: The ArrowListDType.
    """
    if pa_type_is_fixed_shape_tensor(pa_type):
        return ArrowListDType.FIXED_SHAPE_TENSOR
    return ArrowListDType.LIST


def get_max_depth_of_nested_list(data: Union[npt.NDArray, List]) -> int:
    """Gets the maximum depth of a nested list.

    :param data: The nested list to get the maximum depth of.

    :return: The maximum depth of the nested list.
    """
    if isinstance(data, (np.ndarray, list)):
        depths = [get_max_depth_of_nested_list(element) for element in data]
        return 1 + max(depths)
    return 0


def get_shape_of_multi_dim_chunked_array(
    array: pa.ChunkedArray, arrow_list_dtype: ArrowListDType
) -> Tuple[int, ...]:
    """Gets the shape of a multi-dimensional pa.ChunkedArray.

    :param array: The multi-dimensional array to get the shape of.
    :param arrow_list_dtype: The ArrowListDType of the array.

    :return: The shape of the multi-dimensional pa.ChunkedArray.
    """
    if arrow_list_dtype == ArrowListDType.FIXED_SHAPE_TENSOR:
        return tuple(array.type.shape)
    return get_shape_of_nested_pa_list_scalar(array[0])


def get_shape_of_nested_pa_list_scalar(
    data: pa.ListScalar,
) -> Tuple[int, ...]:
    """Gets the shape of a nested pa.ChunkedArray.

    :param data: The nested list to get the shape of.

    :return: The shape of the nested pa.ChunkedArray.
    """
    if isinstance(data, pa.ListScalar) and data is not None:
        return (len(data),) + get_shape_of_nested_pa_list_scalar(data[0])
    return ()


def is_class_member(obj: Callable) -> bool:
    """Checks if the given object is a class member.

    :param obj: The object to check.

    :return: True if the given object is a class member, False otherwise.
    """
    return inspect.isclass(obj)


def is_key_order_incorrect(data: Dict[str, Any], expected_keys: list) -> bool:
    """Checks if the keys of the given dictionary are in the correct order.

    :param data: The dictionary to check.
    :param expected_keys: The expected keys of the dictionary.

    :return: True if the keys of the given dictionary are in the correct order,
        False otherwise.
    """
    return list(data.keys()) != expected_keys


def is_numpy_array_multi_dim(data: npt.NDArray) -> bool:
    """Checks if the given numpy array is multi-dimensional.

    :param data: The numpy array to check.

    :return: True if the given numpy array is multi-dimensional, False otherwise.
    """
    if data.dtype == np.dtype("O"):
        return any(isinstance(item, (np.ndarray, list)) for item in data)
    return data.ndim > 1


def is_object_derived_from_class(obj: Any, cls: Any) -> bool:
    """Checks if the given object is derived from the given class.

    :param obj: The object to check.
    :param cls: The class to check.

    :return: True if the given object is derived from the given class, False otherwise.
    """
    return issubclass(obj, cls) and obj.__name__ != cls.__name__


def import_py_module_from_path(file_path: Path, spec_name: str) -> Any:
    """Import a python module from a given file path.

    :param file_path: The path of the file to import the module from.
    :param spec_name: The name to import the module as.

    :return: The imported module.
    """
    spec = importlib.util.spec_from_file_location(spec_name, file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore

    try:
        spec.loader.exec_module(module)  # type: ignore
    except FileNotFoundError as exc:
        message = f"Could not load module from file: {file_path.as_posix()}."
        logger.error(message, exc_info=True)
        raise exc

    return module


def load_custom_inference_builder(
    matching_files: Set[Path],
) -> InferenceBuilder:
    """Load custom inference builder from the python modules specified in a
    given custom inference config.

    :param matching_files: A set of paths to the python files that contain the
    custom InferenceBuilder and its related components.

    :return: An InferenceBuilder subclass instance.
    """
    logger.info("Loading custom InferenceBuilder from Python files...")

    inference_builder = None

    for py_file in matching_files:  # type: ignore
        module = import_py_module_from_path(py_file, "custom_inference")
        for _, obj in inspect.getmembers(module, is_class_member):
            if is_object_derived_from_class(obj, InferenceBuilder):
                if inference_builder is None:
                    inference_builder = obj()
                else:
                    message = "Multiple InferenceBuilder subclasses found in the given files."  # noqa: E501
                    logger.error(message)
                    raise ValueError(message)

    if inference_builder is None:
        message = "No InferenceBuilder subclass found in the given files."
        logger.error(message)
        raise AttributeError(message)

    logger.info("Loading successful.")

    return inference_builder


def log_error(exception_type: Type[Exception], message: str) -> Any:
    """This helper function logs the error and raises the given exception type.

    :param exception_type: The type of the exception to raise.
    :param message: The message to log.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                logger.error(message, exc_info=True)
                raise exception_type(message) from exc

        return wrapper

    return decorator


def nested_pa_list_type_constructor(
    max_dim: int, data_type: pa.DataType
) -> pa.ListType:
    """This helper function constructs a nested PyArrow list type.

    :param max_dim: The number of dimensions of the nested list.
    :param data_type: The data type of the nested list.

    :return: The nested PyArrow ListType object.
    """
    while max_dim > 1:
        max_dim -= 1
        return pa.list_(nested_pa_list_type_constructor(max_dim, data_type))
    return data_type


def pa_type_is_fixed_shape_tensor(data_type: pa.DataType) -> bool:
    """Checks if the given PyArrow data type is a fixed shape tensor type.

    :param data_type: The data type to check.

    :return: True if the given data type is a fixed shape tensor type, False otherwise.
    """
    return isinstance(data_type, pa.FixedShapeTensorType)


def pa_type_is_list(data_type: pa.DataType) -> bool:
    """Checks if the given PyArrow data type is a list type.

    :param data_type: The data type to check.

    :return: True if the given data type is a list type, False otherwise.
    """
    return isinstance(data_type, (pa.ListType, pa.FixedSizeListType))


def raise_file_format_error_if_file_format_incorrect(
    file_path: Path, supported_file_formats: Set[str]
) -> None:
    """Raise a FileFormatError if the format of the given file is not supported, i.e.,
        the format of the given file is not in the supported_file_formats.

    :param file_path: The path of the file which we want to check the validity
        of its format. The file must exist.
    :param supported_file_formats: A list of supported file formats.
        The concreate classes that deal with files should define this attribute.

    :raises FileFormatError: If the format of the given file is not in the
        supported_file_formats list, then a FileFormatError is raised.
    """
    file_format = file_path.suffix[1:]
    if file_format not in supported_file_formats:
        message = (
            f"File format {file_format} is not supported. "
            f"Supported file formats are: {supported_file_formats}."
        )
        logger.error(message)
        raise FileFormatError(message)


def raise_directory_not_exists_if_no_dir(
    directory: Path,
) -> None:
    """Raise an error if the directory doesn't exist.

    :param directory: Path to the directory.

    :raises DirectoryNotExistError: If there is no directory at the given path, then
        DirectoryNotExistError is raised.
    """
    if not directory.is_dir():
        message = f"There is no directory at: '{directory.as_posix()}'."
        logger.error(message)
        raise DirectoryNotExistError(message)


def raise_path_not_exist_error_if_no_path(
    path: Path,
) -> None:
    """This helper function raises an error if the path passed doesn't exist.

    :param path: Path of a file.

    :raises PathDoesNotExistError: If there is no file at the given path, then
        PathDoesNotExistError is raised.
    """
    if not path.exists():
        message = f"There is no file or directory at: '{path.as_posix()}'."
        logger.error(message)
        raise PathNotExistError(message)
