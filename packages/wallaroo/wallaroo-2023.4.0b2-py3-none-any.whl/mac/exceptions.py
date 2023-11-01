"""This module defines custom exceptions for the mac package."""


class DirectoryNotExistError(Exception):
    """This exception is raised if the directory does not exist."""

    def __init__(self, message: str) -> None:
        """Initializes the DirectoryNotExistError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class FileFormatError(Exception):
    """This exception is raised if the file format of the given file path
    is not supported."""

    def __init__(self, message: str) -> None:
        """Initializes the FileFormatError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class InferenceDataValidationError(Exception):
    """This exception is raised if the InferenceData is not valid."""

    def __init__(self, message: str) -> None:
        """Initializes the InferenceDataValidationError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class InferencePostprocessingError(Exception):
    """This exception is raised if the Postprocessor.postprocess() raises an error."""

    def __init__(self, message: str) -> None:
        """Initializes the InferencePostprocessingError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class InferencePreprocessingError(Exception):
    """This exception is raised if the Preprocessor.preprocess() raises an error."""

    def __init__(self, message: str) -> None:
        """Initializes the InferencePreprocessingError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class InferenceTypeError(Exception):
    """This exception is raised if the Inference doesn't have the correct type."""

    def __init__(self, message: str) -> None:
        """Initializes the InferenceTypeError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class MLflowModelSignatureError(Exception):
    """This exception is raised if the ModelSignature is not in the right format
    for MLflow."""

    def __init__(self, message: str) -> None:
        """Initializes the MLflowModelSignatureError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class ModelPredictionError(Exception):
    """This exception is raised if the model prediction is raising an error."""

    def __init__(self, message: str) -> None:
        """Initializes the ModelPredictionError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class ModelNotAssignedError(Exception):
    """This exception is raised if the model is not assigned to the inference."""

    def __init__(self, message: str) -> None:
        """Initializes the ModelNotAssignedError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class PandasRecordsConversionError(Exception):
    """This exception is raised if converting InferenceData to/from pandas records
    is raising an error."""

    def __init__(self, message: str) -> None:
        """Initializes the PandasRecordsConversionError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class PathNotExistError(Exception):
    """This exception is raised if the path does not exist."""

    def __init__(self, message: str) -> None:
        """Initializes the PathNotExistError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class ArrowRecordBatchConversionError(Exception):
    """This exception is raised if converting InferenceData to/from pyarrow
    RecordBatch is raising an error."""

    def __init__(self, message: str) -> None:
        """Initializes the ArrowRecordBatchConversionError class.

        :param message: The message of the exception.
        """
        super().__init__(message)


class SubclassTypeNotExistError(Exception):
    """This exception is raised if the subclass type does not exist
    whenever an AbstractFactory is used."""

    def __init__(self, message: str) -> None:
        """Initializes the SubclassTypeNotExistError class.

        :param message: The message of the exception.
        """
        super().__init__(message)
