# This is a centralized file for reusable httpx and responses mocks
# that may be used across multiple tests. i.e. many tests require a workspace, so
# they all need to be able to respond to a query for one.
from . import testutil
import responses
import httpx


def add_default_workspace_responder(api_endpoint="http://api-lb:8080"):
    responses.add(
        responses.POST,
        f"{api_endpoint}/v1/graphql",
        status=200,
        match=[testutil.query_name_matcher("UserDefaultWorkspace")],
        json={
            "data": {
                "user_default_workspace": [
                    {
                        "workspace": {
                            "archived": False,
                            "created_at": "2022-02-15T09:42:12.857637+00:00",
                            "created_by": "bb2dec32-09a1-40fd-8b34-18bd61c9c070",
                            "name": "345fr",
                            "id": 1,
                            "pipelines": [],
                            "models": [],
                        }
                    }
                ]
            }
        },
    )


def add_create_pipeline_responder(
    respx_mock,
    pipeline_pk_id=1,
    pipeline_variant_pk_id=1,
    api_endpoint="http://api-lb:8080",
    pipeline_variant_version=1,
):
    respx_mock.post(f"{api_endpoint}/v1/api/pipelines/create").mock(
        return_value=httpx.Response(
            200,
            json={
                "pipeline_pk_id": pipeline_pk_id,
                "pipeline_variant_pk_id": pipeline_variant_pk_id,
                "pipeline_variant_version": pipeline_variant_version,
            },
        )
    )


def add_deploy_responder(
    respx_mock, expected_deployment_id=1, api_endpoint="http://api-lb:8080"
):
    respx_mock.post(f"{api_endpoint}/v1/api/pipelines/deploy").mock(
        return_value=httpx.Response(200, json={"id": expected_deployment_id})
    )


def add_deployment_status_responder(
    respx_mock, pipeline_id="test", api_endpoint="http://api-lb:8080"
):
    status_response = {
        "status": "Running",
        "details": None,
        "engines": [
            {
                "ip": "10.52.0.43",
                "name": "engine-7b66744596-kk25b",
                "status": "Running",
                "reason": None,
                "pipeline_statuses": {
                    "pipelines": [{"id": pipeline_id, "status": "Running"}]
                },
                "model_statuses": {
                    "models": [
                        {
                            "name": "postprocess",
                            "version": "32a143bb-efa2-482d-85bb-0f0bae42bf40",
                            "sha": "4bd3109602e999a3a5013893cd2eff1a434fd9f06d6e3e681724232db6fdd40d",
                            "status": "Running",
                        },
                        {
                            "name": "demandcurve",
                            "version": "82effafa-7a52-43ea-b44d-dca4aa449b3c",
                            "sha": "d2adc767d255905072857f5a9a81ebc6da5f22e5c582c5948fb8bc7c989657d2",
                            "status": "Running",
                        },
                        {
                            "name": "preprocess",
                            "version": "14f2978d-f377-4bf7-9759-8ad1d6dc88f0",
                            "sha": "b36eb8cad3975ace129813089a8515911a6c060a491f777b69cc37a0ae35354e",
                            "status": "Running",
                        },
                    ]
                },
            }
        ],
        "engine_lbs": [
            {
                "ip": "10.52.0.44",
                "name": "engine-lb-77ff988845-4zqvd",
                "status": "Running",
                "reason": None,
            }
        ],
    }

    respx_mock.post(f"{api_endpoint}/v1/api/status/get_deployment").mock(
        return_value=httpx.Response(200, json=status_response)
    )


def add_deployment_status_requests_responder(api_endpoint="http://api-lb:8080"):
    responses.add(responses.POST, f"{api_endpoint}/v1/api/status")


def add_undeploy_responder(respx_mock, api_endpoint="http://api-lb:8080"):
    respx_mock.post(f"{api_endpoint}/v1/api/pipelines/undeploy").mock(
        return_value=httpx.Response(200, json={})
    )


def add_deployment_for_pipeline_responder(api_endpoint="http://api-lb:8080"):
    responses.add(
        responses.POST,
        f"{api_endpoint}/v1/graphql",
        status=200,
        match=[testutil.query_name_matcher("GetDeploymentForPipeline")],
        json={
            "data": {
                "pipeline_by_pk": {
                    "deployment": {
                        "id": 1,
                        "deploy_id": "some-pipeline",
                        "deployed": True,
                        "engine_config": {
                            "engine": {},
                        }
                    }
                }
            },
        },
    )


def add_deployment_by_id_responder(api_endpoint="http://api-lb:8080"):
    responses.add(
        responses.POST,
        "http://api-lb:8080/v1/graphql",
        status=200,
        match=[testutil.query_name_matcher("DeploymentById")],
        json={
            "data": {
                "deployment_by_pk": {
                    "id": 1,
                    "deploy_id": "some-pipeline",
                    "deployed": True,
                    "pipeline": {
                        "pipeline_id": "some-pipeline",
                    },
                },
            },
        },
    )


def add_insert_model_config_response(api_endpoint="http://api-lb:8080"):
    resp = responses.add(
        responses.POST,
        f"{api_endpoint}/v1/api/models/insert_model_config",
        status=200,
        json={
            "model_config": {
                "id": 1,
                "model_version_id": 1,
                "runtime": "mlflow",
                "input_schema": "/////Base64EncodedInputSchema=",
                "output_schema": "/////Base64EncodedOutputSchema=",
            },
        },
    )
    return resp


def add_insert_model_config_response_with_config(
    api_endpoint="http://api-lb:8080", gen_id=1, model_config={}
):
    responses.add(
        responses.POST,
        f"{api_endpoint}/v1/api/models/insert_model_config",
        status=200,
        json={
            "model_config": {
                "id": gen_id,
                "tensor_fields": None,
                "filter_threshold": None,
                **model_config,
            }
        },
    )


def add_get_model_config_response(api_endpoint="http://api-lb:8080"):
    resp = responses.add(
        responses.POST,
        f"{api_endpoint}/v1/api/models/get_config_by_id",
        status=200,
        json={
            "model_config": {
                "id": 1,
                "model_version_id": 1,
                "runtime": "mlflow",
                "input_schema": "/////Base64EncodedInputSchema=",
                "output_schema": "/////Base64EncodedOutputSchema=",
            },
        },
    )
    return resp


def add_get_topic_name_responder(api_endpoint="http://api-lb:8080"):
    resp = responses.add(
        responses.POST,
        f"{api_endpoint}/v1/api/plateau/get_topic_name",
        match=[responses.matchers.json_params_matcher({"pipeline_pk_id": 1})],
        status=200,
        json={"topic_name": "workspace-1-pipeline-x-inference"},
    )

    return resp
