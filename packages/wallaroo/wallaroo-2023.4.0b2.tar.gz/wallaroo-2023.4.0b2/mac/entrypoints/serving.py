"""This module features entrypoints for serving a model using MLflow."""

import logging
from pathlib import Path
from typing import Callable

from mac.config.inference import CustomInferenceConfig, InferenceConfig
from mac.config.service import InferenceServiceConfig, ServerConfig
from mac.config.service.creation import InferenceServiceConfigFactory
from mac.inference.creation import InferenceBuilder
from mac.io.file_loading.json_loader import JSONLoader
from mac.service.creation import InferenceServiceFactory
from mac.types import SupportedServices
from mac.utils.helpers import load_custom_inference_builder

logger = logging.getLogger(__name__)


def serve_inference(
    inference_service_config: InferenceServiceConfig,
    inference_builder: InferenceBuilder,
) -> None:
    """Creates an Inference object from the config,
    and also creates the InferenceService and perform serving.

    :param inference_service_config: An InferenceServiceConfig instance.

    :param inference_builder: An InferenceBuilder instance.
    """
    inference = inference_builder.create(inference_service_config.inference)
    inference_service = InferenceServiceFactory().create(
        inference_service_config.service_type.value,
        config=inference_service_config,
        inference=inference,
    )
    inference_service.serve()


def create_inference_config(
    config_dict: dict,
) -> InferenceConfig:
    """Creates an InferenceConfig from a parsed JSON file.

    :param config_dict: Dictionary loaded from a model JSON config.

    :return: An InferenceConfig instance.
    """
    framework = config_dict["data"]["model"]["model_version"]["conversion"][
        "framework"
    ]
    model_path = config_dict["data"]["model"]["model_version"]["file_info"][
        "file_name"
    ]

    return InferenceConfig(framework=framework, model_path=model_path)


def create_custom_inference_config(config_dict: dict) -> CustomInferenceConfig:
    """Creates a CustomInferenceConfig from a parsed JSON file.

    :param config_dict: Dictionary loaded from a model JSON config.

    :return: An CustomInferenceConfig instance.
    """
    framework = config_dict["data"]["model"]["model_version"]["conversion"][
        "framework"
    ]
    model_path = config_dict["data"]["model"]["model_version"]["file_info"][
        "file_name"
    ]

    return CustomInferenceConfig(
        framework=framework,
        model_path=Path(model_path),
        modules_to_include=[Path("*.py")],
    )


def serve_auto_inference_from_json_config(
    config_path: Path,
    inference_builder: InferenceBuilder,
    inference_config_creator: Callable[
        [dict], InferenceConfig
    ] = create_inference_config,
    service_type: SupportedServices = SupportedServices.MLFLOW,
    host: str = "0.0.0.0",
    port: int = 8080,
) -> None:
    """Entrypoint for serving an auto Inference from
    a model JSON file using a supported service.

    :param config_path: Path to the configuration file.
    :param inference_builder: InferenceBuilder instance.
    :param service_type: Service to use for serving.

    Example of the config file:

    {
            "id": "uuid",
            "metadata": {
                "name": "model_name",
                "visibility": "string",
                "workspace_id": 1234,
                "conversion": {
                    "python_version": "3.8",
                    "framework": "keras",
                    "requirements": [],
                },
                "file_info": {
                    "version": "uuid",
                    "sha": "0000000000000000...",
                    "file_name": "model_file.h5"
                }
            }
        }
    """
    logger.info(
        f"Serving auto Inference with `{service_type.value}` from JSON config..."
    )
    config = JSONLoader().load(config_path)
    inference_config = inference_config_creator(config)
    inference_service_config = InferenceServiceConfigFactory().create(
        service_type.value,
        inference=inference_config,
        server=ServerConfig(host=host, port=port),
    )
    serve_inference(
        inference_service_config=inference_service_config,
        inference_builder=inference_builder,
    )

    logger.info("Serving successful.")


def serve_custom_inference_from_json_config(
    config_path: Path,
    service_type: SupportedServices = SupportedServices.MLFLOW,
    host: str = "0.0.0.0",
    port: int = 8080,
) -> None:
    """Entrypoint for serving a custom Inference from a
    model JSON file using a supported service.

    :param config_path: Path to the model JSON file coming from the pipeline.
    :param service_type: Service to use for serving.
    """
    logger.info(
        f"Serving custom Inference with {service_type.value} from JSON config..."
    )
    config = JSONLoader().load(config_path)
    custom_inference_config = create_custom_inference_config(config)
    inference_service_config = InferenceServiceConfigFactory().create(
        service_type.value,
        inference=custom_inference_config,
        server=ServerConfig(host=host, port=port),
    )
    custom_inference_builder = load_custom_inference_builder(
        inference_service_config.inference.matching_files
    )
    serve_inference(
        inference_service_config=inference_service_config,
        inference_builder=custom_inference_builder,
    )

    logger.info("Serving successful.")
