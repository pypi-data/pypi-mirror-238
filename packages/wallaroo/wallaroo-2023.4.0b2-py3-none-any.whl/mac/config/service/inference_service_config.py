"""This module contains the InferenceServiceConfig class.
InferenceServiceConfig is the base class for all inference service configurations
such as MLflow service.
"""

from abc import abstractmethod

from pydantic import BaseModel, ConfigDict

from mac.config.inference import InferenceConfig
from mac.config.service.server_config import ServerConfig
from mac.types import SupportedServices


class InferenceServiceConfig(BaseModel):
    """This class represents the configuration for an Inference Service object
    (e.g., MLflow service).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    inference: InferenceConfig
    server: ServerConfig = ServerConfig()

    @property
    @abstractmethod
    def service_type(self) -> SupportedServices:
        """This property specifies the type of service this configuration is for."""
