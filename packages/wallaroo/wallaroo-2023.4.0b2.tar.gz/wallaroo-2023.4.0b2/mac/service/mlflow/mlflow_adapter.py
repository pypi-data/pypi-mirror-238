"""This module features MLflowAdapter, that makes the Inference interface
compatible with MLflow REST API.
"""

import logging
import random

import pandas as pd
from mlflow.models.utils import PyFuncInput, PyFuncOutput
from mlflow.pyfunc.model import PythonModel, PythonModelContext

from mac.exceptions import PandasRecordsConversionError
from mac.inference import Inference
from mac.types import InferenceData
from mac.utils.helpers import (
    convert_dataframe_to_dict_of_numpy_arrays,
    log_error,
)

logger = logging.getLogger(__name__)


class MLflowAdapter(PythonModel):
    """This class acts as an adapter that makes the Inference interface
    compatible with MLflow REST API.

    Attributes:
        - inference: An Inference instance.
    """

    def __init__(
        self,
        inference: Inference,
    ):
        """Initializes an MLflowAdapter instance."""
        self._inference = inference

    def predict(
        self, context: PythonModelContext, model_input: PyFuncInput
    ) -> PyFuncOutput:
        """Evaluates a pyfunc-compatible input and produces a pyfunc-compatible output.
        For more information about the pyfunc input/output API,
        see the :ref:`pyfunc-inference-api`

        :param context: A class:`~PythonModelContext` instance containing artifacts
        that the model can use to perform inference.
        :param model_input: A pyfunc-compatible input for the model to
        perform inference.

        :return: A pyfunc-compatible output of the model inference.
        """
        logger.info("Converting pandas records to InferenceData...")
        inference_data = self._convert_pandas_records_to_inference_data(
            df_records=model_input
        )

        logger.info("Parsing InferenceData to Inference...")
        predictions = self._inference.predict(input_data=inference_data)

        logger.info("Converting InferenceData to pandas records...")
        df_records = self._convert_predictions_to_df_records(predictions)
        logger.info("Output data ready to be consumed.")

        return df_records

    @log_error(
        PandasRecordsConversionError,
        "Failed to convert pandas records to InferenceData.",
    )
    def _convert_pandas_records_to_inference_data(
        self, df_records: pd.DataFrame
    ) -> InferenceData:
        return convert_dataframe_to_dict_of_numpy_arrays(df_records)

    @staticmethod
    @log_error(
        PandasRecordsConversionError,
        "Failed to convert InferenceData to pandas records.",
    )
    def _convert_predictions_to_df_records(
        predictions: InferenceData,
    ) -> pd.DataFrame:
        random_key = random.choice(list(predictions.keys()))
        num_samples = len(predictions[random_key])
        records = [
            {key: value[i] for key, value in predictions.items()}
            for i in range(num_samples)
        ]
        return pd.DataFrame(records)
