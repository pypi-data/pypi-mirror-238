"""This module implements the ArrowFlightService class, for serving models using
Arrow Flight RPC."""

import logging

from mac.config.service import ArrowFlightServiceConfig
from mac.inference import Inference
from mac.service import InferenceService
from mac.service.arrow_flight.server import ArrowFlightServer

logger = logging.getLogger(__name__)


class ArrowFlightService(InferenceService):
    """This class implements the ArrowFlightService, in order to serve Inference
    objects using Arrow Flight RPC.

    Attributes:
        - arrow_flight_server: An ArrowFlightServer instance.
    """

    def __init__(
        self,
        arrow_flight_server: ArrowFlightServer,
    ) -> None:
        """Initialize ArrowFlightService class."""
        self._arrow_flight_server = arrow_flight_server

    def serve(self) -> None:
        """This method serves an Inference object using the Arrow Flight RPC service."""
        logging.info(
            f"[📡] Starting server on `{self._arrow_flight_server.location}`..."  # type: ignore [union-attr] # noqa: E501
        )
        self._arrow_flight_server.serve()  # type: ignore [union-attr]


def create_arrow_flight_service(
    config: ArrowFlightServiceConfig, inference: Inference
) -> ArrowFlightService:
    """Initializes an ArrowFlightService based on the given ArrowFlightServiceConfig
    and a given Inference object.

    :param config: A ArrowFlightServiceConfig instance.
    :param inference: An Inference instance.

    :return: An ArrowFlightService instance.
    """
    logger.info("Creating Arrow Flight RPC service...")

    server = ArrowFlightServer(
        inference=inference, server_config=config.server
    )
    service = ArrowFlightService(server)

    logger.info("Successfully created Arrow Flight RPC service.")

    return service
