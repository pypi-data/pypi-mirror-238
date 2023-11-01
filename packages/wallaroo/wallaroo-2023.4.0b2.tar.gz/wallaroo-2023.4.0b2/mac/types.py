"""This module defines custom types for the Model Auto Conversion (MAC) package.

Currently, the following types are available:
- InferenceData: This type is used to define the data that is used for inference.
- SupportedFrameworks: This type is used to define the supported frameworks.
- SupportedServices: This type is used to define the supported services.
"""

from enum import Enum
from typing import Callable, Dict, Tuple, Union

import numpy.typing as npt
import pyarrow as pa
from typing_extensions import TypeAlias

# Define the type for inference data.
InferenceData: TypeAlias = Dict[str, npt.NDArray]

# Arrow from/to NDArray converters.
ArrowToNDArrayConverter: TypeAlias = Callable[[pa.ChunkedArray], npt.NDArray]
NDArrayToArrowConverter: TypeAlias = Callable[
    [npt.NDArray],
    Tuple[pa.DataType, Union[pa.Array, pa.ListArray, pa.ExtensionArray]],
]


class ArrowListDType(str, Enum):
    """This class defines the possible PyArrow list data types."""

    LIST = "list"
    FIXED_SHAPE_TENSOR = "fixed-shape-tensor"


class IOArrowDType(str, Enum):
    """This class defines the possible Arrow pa.ChunkedArray
    data types for the input and output to/from
    an ArrowFlightServer."""

    LIST = ArrowListDType.LIST.value
    FIXED_SHAPE_TENSOR = ArrowListDType.FIXED_SHAPE_TENSOR.value
    SCALAR = "scalar"


class SupportedFrameworks(str, Enum):
    """This class defines an Enum for supported frameworks. The frameworks are used
    to load models. The frameworks can be keras, sklearn, etc.
    """

    KERAS = "keras"
    SKLEARN = "sklearn"
    PYTORCH = "pytorch"
    XGBOOST = "xgboost"
    HUGGING_FACE = "hugging-face"
    CUSTOM = "custom"


class SupportedServices(str, Enum):
    """This class defines an Enum for supported services that
    serve ML models for inference purposes.
    """

    MLFLOW = "mlflow"
    FLIGHT = "flight"
