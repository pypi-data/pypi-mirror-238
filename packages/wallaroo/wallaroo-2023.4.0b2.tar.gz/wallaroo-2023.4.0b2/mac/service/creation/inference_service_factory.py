"""This module features the InferenceServiceFactory for creating
concrete InferenceService subclass instances."""

from mac.service.arrow_flight.arrow_flight_service import (
    create_arrow_flight_service,
)
from mac.service.mlflow.mlflow_service import create_mlflow_service
from mac.types import SupportedServices
from mac.utils import AbstractFactory

subclass_creators = {
    SupportedServices.MLFLOW.value: create_mlflow_service,
    SupportedServices.FLIGHT.value: create_arrow_flight_service,
}


class InferenceServiceFactory(AbstractFactory):
    """This class implements the AbstractFactory interface
    for creating concrete InferenceService subclass instances."""

    @property
    def subclass_creators(self) -> dict:
        """Returns a dictionary of supported inference services and
        their corresponding subclass creators.

        :return: A dictionary of subclass creators.
        """
        return subclass_creators
