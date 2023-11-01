"""This module implements the helper class for Gunicorn serving."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from gunicorn.app.base import BaseApplication
from six import iteritems

if TYPE_CHECKING:
    from flask.app import Flask


class GunicornApplication(BaseApplication):
    """This class implements a wrapper for a Flask
    app in order to be served with Gunicorn.

    Attributes:
        - app: A Flask app instance.
        - options: A dictionary with Gunicorn options.
    """

    # pylint: disable=W0223

    def __init__(
        self, app: Optional[Flask], options: Optional[dict] = None
    ) -> None:
        """Initialize the class with a Flask app."""
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self) -> None:
        """Loads the configuration for Gunicorn."""
        config = {
            key: value
            for key, value in iteritems(self.options)
            if key in self.cfg.settings and value is not None
        }

        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self) -> Optional[Flask]:
        """Getter for the Flask app."""
        return self.application
