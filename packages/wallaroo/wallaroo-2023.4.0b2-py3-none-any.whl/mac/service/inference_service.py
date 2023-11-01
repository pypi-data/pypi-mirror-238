"""This module defines InferenceService interface. All inference services must
implement this interface, e.g., MLflowService.
"""

from abc import ABC, abstractmethod


class InferenceService(ABC):
    """Abstract class for an Inference service."""

    @abstractmethod
    def serve(self) -> None:
        """This method serves an Inference object using a service."""
