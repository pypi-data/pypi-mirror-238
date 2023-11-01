"""This module features the InferenceServiceConfigFactory for creating
concrete InferenceServiceConfig subclass instances."""

from mac.config.service import ArrowFlightServiceConfig, MLflowServiceConfig
from mac.types import SupportedServices
from mac.utils import AbstractFactory

subclass_creators = {
    SupportedServices.MLFLOW.value: MLflowServiceConfig,
    SupportedServices.FLIGHT.value: ArrowFlightServiceConfig,
}


class InferenceServiceConfigFactory(AbstractFactory):
    """This class implements the AbstractFactory interface
    for creating concrete InferenceServiceConfig subclass instances."""

    @property
    def subclass_creators(self) -> dict:
        """Returns a dictionary of supported inference services and
        their corresponding subclass creators.

        :return: A dictionary of subclass creators.
        """
        return subclass_creators
