"""This module features the ArrowFlightServiceConfig class."""

import logging

from mac.config.service.inference_service_config import InferenceServiceConfig
from mac.types import SupportedServices

logger = logging.getLogger(__name__)


class ArrowFlightServiceConfig(InferenceServiceConfig):
    """This class represents the configuration of ArrowFlightService."""

    @property
    def service_type(self) -> SupportedServices:
        """This property specifies the type of service this configuration is for."""
        return SupportedServices.FLIGHT
