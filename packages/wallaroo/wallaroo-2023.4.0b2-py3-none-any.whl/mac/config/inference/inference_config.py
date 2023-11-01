"""This module contains the InferenceConfig class.
This class defines configuration parameters for an Inference object.
"""

from typing import Union

from pydantic import BaseModel, ConfigDict, DirectoryPath, FilePath

from mac.types import SupportedFrameworks


class InferenceConfig(BaseModel):
    """This class defines configuration parameters for an Inference object."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True, extra="forbid", protected_namespaces=()
    )

    # The framework of the model to be loaded. See SupportedFrameworks for more info.
    framework: SupportedFrameworks

    # The path to the model.
    model_path: Union[FilePath, DirectoryPath]
