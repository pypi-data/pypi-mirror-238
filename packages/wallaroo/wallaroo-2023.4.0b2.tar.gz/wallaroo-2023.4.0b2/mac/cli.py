"""This module features the CLI entrypoints for the mac package.
You can use the CLI entrypoints to convert models and run inference on them.
"""

from pathlib import Path

import typer

from mac.entrypoints.serving import serve_custom_inference_from_json_config
from mac.types import SupportedServices

app = typer.Typer()


@app.command()
def serve(
    config_path: Path = typer.Option(..., "--config-path", exists=True),
    service: SupportedServices = SupportedServices.MLFLOW,
    host: str = "0.0.0.0",
    port: int = 8080,
):
    """Serve a custom Inference with a specified service.

    :param config_path: Path to the JSON config file.
    :param service: Service to use for serving the base Inference.
    :param host: Host to serve the Inference on.
    :param port: Port to serve the Inference on.

    :raises NotImplementedError: If the specified service is not supported.
    """
    if service.value in [member.value for member in SupportedServices]:
        serve_custom_inference_from_json_config(
            config_path=config_path, service_type=service, host=host, port=port
        )
    else:
        raise NotImplementedError(f"Service {service} is not supported.")


@app.command(hidden=True)
def secret():
    """This is a secret command, that helps calling the serve command by its name."""
    raise NotImplementedError()
