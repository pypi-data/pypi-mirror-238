import json
import os
import string
import tempfile
import unittest
from datetime import datetime, timezone
from typing import cast
from unittest import mock
from unittest.mock import patch

# This file uses unittest, not pytest, so it can't use the pytest.mark fixture
import httpx
import pyarrow as pa
import responses
import respx

import wallaroo
import wallaroo.pipeline
from wallaroo.client import (
    WALLAROO_AUTH_URL,
    WALLAROO_SDK_AUTH_ENDPOINT,
    WALLAROO_SDK_AUTH_TYPE,
    WALLAROO_URL,
)
from wallaroo.framework import Framework
from wallaroo.object import InvalidNameError, ModelConversionTimeoutError
from wallaroo.user import User

from . import testutil
from .reusable_responders import (
    add_insert_model_config_response, add_get_model_config_response
)


with open("unit_tests/outputs/get_assay_results.json", "r") as fp:
    SAMPLE_GET_ASSAYS_RESULTS = json.loads(fp.read())


def test_compute_urls():
    if WALLAROO_SDK_AUTH_TYPE in os.environ:
        os.environ.pop(WALLAROO_SDK_AUTH_TYPE)
    if WALLAROO_SDK_AUTH_ENDPOINT in os.environ:
        os.environ.pop(WALLAROO_SDK_AUTH_ENDPOINT)
    if WALLAROO_AUTH_URL in os.environ:
        os.environ.pop(WALLAROO_AUTH_URL)
    if WALLAROO_URL in os.environ:
        os.environ.pop(WALLAROO_URL)

    # if nothing is specified
    (auth_type, api_endpoint, auth_endpoint) = wallaroo.client.Client.get_urls(
        None, "http://api-lb:8080", ""
    )
    assert auth_type is None
    assert api_endpoint == "http://api-lb:8080"
    assert auth_endpoint != ""

    auth_endpoint = None
    api_endpoint = None
    # if the type is specified
    os.environ[WALLAROO_SDK_AUTH_TYPE] = "user_password"
    (auth_type, api_endpoint, auth_endpoint) = wallaroo.client.Client.get_urls(
        None, "http://api-lb:8080", ""
    )
    assert auth_type == "user_password"
    assert api_endpoint == "http://api-lb:8080"
    assert auth_endpoint == "http://api-lb:8080"

    auth_endpoint = None
    api_endpoint = None
    # if type and no address in env
    os.environ[WALLAROO_SDK_AUTH_TYPE] = "sso"
    (auth_type, api_endpoint, auth_endpoint) = wallaroo.client.Client.get_urls(
        None, "http://api-lb:8080", ""
    )
    assert auth_type == "sso"
    assert auth_endpoint == "http://api-lb:8080"

    # if type and address in env
    key_cloak_adress = "https://yellow-elephant.wallaroo.dev/keycloak"
    os.environ[WALLAROO_SDK_AUTH_TYPE] = "sso"
    os.environ[WALLAROO_SDK_AUTH_ENDPOINT] = key_cloak_adress
    (auth_type, api_endpoint, auth_endpoint) = wallaroo.client.Client.get_urls(
        None, "http://api-lb:8080", ""
    )
    assert auth_type == "sso"
    assert auth_endpoint == key_cloak_adress

    # if type and address in params
    key_cloak_adress = "https://yellow-elephant.wallaroo.dev/keycloak"
    os.environ[WALLAROO_SDK_AUTH_TYPE] = "sso"
    os.environ[WALLAROO_SDK_AUTH_ENDPOINT] = key_cloak_adress
    (auth_type, api_endpoint, auth_endpoint) = wallaroo.client.Client.get_urls(
        "foo", "baz", "bar"
    )
    assert auth_type == "foo"
    assert auth_endpoint == "bar"

    if WALLAROO_SDK_AUTH_TYPE in os.environ:
        os.environ.pop(WALLAROO_SDK_AUTH_TYPE)
    if WALLAROO_SDK_AUTH_ENDPOINT in os.environ:
        os.environ.pop(WALLAROO_SDK_AUTH_ENDPOINT)


class TestClient(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now()
        self.gql_client = testutil.new_gql_client(
            endpoint="http://api-lb:8080/v1/graphql"
        )
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client,
            auth_endpoint="http://mock-keycloak:1234",
            auth_type="test_auth",
        )

    def add_list_pipeline_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ListPipelines")],
            json={"data": {"pipeline": [{"id": 1}, {"id": 2}]}},
        )

    def add_list_tags_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ListTags")],
            json={
                "data": {
                    "tag": [
                        {
                            "id": 1,
                            "tag": "Great new tag",
                            "model_tags": [
                                {
                                    "model": {
                                        "id": 1,
                                        "model_id": "ccfraudmodel",
                                        "models_pk_id": 1,
                                        "model_version": "efb618e5-ba1a-4e05-9c3a-49dd1a053bfc",
                                    }
                                }
                            ],
                            "pipeline_tags": [
                                {
                                    "pipeline": {
                                        "id": 1,
                                        "pipeline_id": "ccfraudmodel",
                                        "pipeline_versions": [
                                            {
                                                "id": 1,
                                                "version": "ad892ca6-62b3-4ff9-8bb5-347eb851bd48",
                                            },
                                            {
                                                "id": 2,
                                                "version": "612c163b-92e1-4ee3-a542-d84c8704a3e9",
                                            },
                                        ],
                                    }
                                }
                            ],
                        }
                    ]
                }
            },
        )

    def add_tag_by_id_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("TagById")],
            json={
                "data": {
                    "tag_by_pk": {
                        "id": 1,
                        "tag": "Great new tag",
                        "model_tags": [
                            {
                                "model": {
                                    "id": 1,
                                    "model_id": "ccfraudmodel",
                                    "models_pk_id": 1,
                                    "model_version": "efb618e5-ba1a-4e05-9c3a-49dd1a053bfc",
                                }
                            }
                        ],
                        "pipeline_tags": [
                            {
                                "pipeline": {
                                    "id": 1,
                                    "pipeline_id": "ccfraudmodel",
                                    "pipeline_versions": [
                                        {
                                            "id": 1,
                                            "version": "ad892ca6-62b3-4ff9-8bb5-347eb851bd48",
                                        },
                                        {
                                            "id": 2,
                                            "version": "612c163b-92e1-4ee3-a542-d84c8704a3e9",
                                        },
                                    ],
                                }
                            }
                        ],
                    }
                }
            },
        )

    def add_list_assays_responder(self, respx_mock):
        assay_resp = [
            {
                "id": 2,
                "name": "Assay 965409",
                "active": True,
                "status": '{"run_at": "2022-08-17T14:48:34.239664761+00:00",  "num_ok": 17, "num_warnings": 0, "num_alerts": 13}',
                "warning_threshold": None,
                "alert_threshold": 0.25,
                "pipeline_id": 15,
                "pipeline_name": "modelinsightse2e06104",
                "last_run": "2022-08-17T14:48:34.239665+00:00",
                "next_run": "2022-08-17T00:00:00+00:00",
                "run_until": None,
                "updated_at": "2022-08-17T14:48:30.962965+00:00",
            },
            {
                "id": 1,
                "name": "Assay 109990",
                "active": True,
                "status": '{"run_at": "2022-08-16T14:31:59.750085918+00:00",  "num_ok": 17, "num_warnings": 0, "num_alerts": 13}',
                "warning_threshold": None,
                "alert_threshold": 0.25,
                "pipeline_id": 3,
                "pipeline_name": "mypipeline",
                "last_run": "2022-08-16T14:31:59.750086+00:00",
                "next_run": "2022-08-17T00:00:00+00:00",
                "run_until": None,
                "updated_at": "2022-08-16T14:31:57.956613+00:00",
            },
        ]

        respx_mock.post(f"{self.test_client.api_endpoint}/v1/api/assays/list").mock(
            return_value=httpx.Response(200, json=assay_resp)
        )

    def add_deployment_for_pipeline_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("GetDeploymentForPipeline")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "deployment": {
                            "id": 2,
                            "deploy_id": "pipeline-258146-2",
                            "deployed": True,
                            "engine_config": {
                                "engine": {},
                            }
                        }
                    }
                },
            },
        )

    def add_pipeline_by_id_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineById")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "id": 3,
                        "pipeline_id": "pipeline-258146-2",
                        "created_at": "2022-04-18T13:55:16.880148+00:00",
                        "updated_at": "2022-04-18T13:55:16.915664+00:00",
                        "visibility": "private",
                        "owner_id": "'",
                        "pipeline_versions": [{"id": 2}],
                        "pipeline_tags": [
                            {"tag": {"id": 1, "tag": "byhand222"}},
                            {"tag": {"id": 2, "tag": "foo"}},
                        ],
                    }
                }
            },
        )

    def add_pipeline_variant_by_id_responder(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineVariantById")],
            json={
                "data": {
                    "pipeline_version_by_pk": {
                        "id": 2,
                        "created_at": self.now.isoformat(),
                        "updated_at": self.now.isoformat(),
                        "version": "v1",
                        "definition": {
                            "id": "test-pipeline",
                            "steps": [
                                {
                                    "id": "metavalue_split",
                                    "args": [
                                        "card_type",
                                        "default",
                                        "gold",
                                        "experiment",
                                    ],
                                    "operation": "map",
                                }
                            ],
                        },
                        "pipeline": {"id": 1},
                        "deployment_pipeline_versions": [],
                    }
                }
            },
        )

    def add_pipeline_models_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineModels")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "id": 3,
                        "deployment": {
                            "deployment_model_configs_aggregate": {
                                "nodes": [
                                    {
                                        "model_config": {
                                            "model": {
                                                "model": {"name": "ccfraud1-258146"}
                                            }
                                        }
                                    },
                                    {
                                        "model_config": {
                                            "model": {
                                                "model": {"name": "ccfraud2-258146"}
                                            }
                                        }
                                    },
                                ]
                            },
                        },
                    }
                }
            },
        )

    def add_user_responder(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/api/users/query",
            status=200,
            json={
                "users": {
                    "a6fa51c3-532b-410a-a5b2-c79277f90e45": {
                        "id": "a6fa51c3-532b-410a-a5b2-c79277f90e45",
                        "createdTimestamp": 1649782475369,
                        "username": "ci",
                        "enabled": True,
                        "totp": False,
                        "emailVerified": True,
                        "firstName": "c",
                        "lastName": "i",
                        "email": "ci@x.com",
                        "disableableCredentialTypes": [],
                        "requiredActions": [],
                        "notBefore": 0,
                        "access": {
                            "manageGroupMembership": True,
                            "view": True,
                            "mapRoles": True,
                            "impersonate": True,
                            "manage": True,
                        },
                    },
                    "6934dc86-0953-4d0a-9de6-3825a19c3ab9": {
                        "id": "6934dc86-0953-4d0a-9de6-3825a19c3ab9",
                        "createdTimestamp": 1649782764151,
                        "username": "di",
                        "enabled": True,
                        "totp": False,
                        "emailVerified": False,
                        "firstName": "d",
                        "lastName": "i",
                        "email": "di@z.z",
                        "disableableCredentialTypes": [],
                        "requiredActions": [],
                        "notBefore": 0,
                        "access": {
                            "manageGroupMembership": True,
                            "view": True,
                            "mapRoles": True,
                            "impersonate": True,
                            "manage": True,
                        },
                    },
                }
            },
        )

    def add_default_workspace_responder(self):
        resp = responses.Response(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/graphql",
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
        responses.add(resp)
        return resp

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_list_models(self, respx_mock):
        self.add_default_workspace_responder()
        model_list_resp = {
            "models": [
                {
                    "id": 0,
                    "owner_id": "string",
                    "created_at": "2022-10-17T15:28:44+0000",
                    "updated_at": "2022-10-17T15:28:44+0000",
                    # This maps to the old model_id
                    "name": "string",
                    # These are only available for individual versions.
                    # "sha": "string",
                    # "models_pk_id": 0,
                    # "model_version": "string",
                    # "model_id": "string",
                    # "file_name": "string",
                },
                {
                    "id": 1,
                    "owner_id": "string",
                    "created_at": "2022-10-17T15:28:44+0000",
                    "updated_at": "2022-10-17T15:28:44+0000",
                    # This maps to the old model_id
                    "name": "string1",
                    "owner_id": "string",
                },
            ]
        }
        respx_mock.post(f"{self.test_client.api_endpoint}/v1/api/models/list").mock(
            return_value=httpx.Response(200, json=model_list_resp)
        )

        variants = self.test_client.list_models()

        self.assertEqual(2, len(variants))
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_list_tags(self):
        self.add_list_tags_responder()
        self.add_tag_by_id_responder()

        tags = self.test_client.list_tags()
        self.assertEqual(1, len(tags))
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_list_deployments(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ListDeployments")],
            json={"data": {"deployment": [{"id": 1}, {"id": 2}]}},
        )

        deployments = self.test_client.list_deployments()

        self.assertEqual(2, len(deployments))
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_model_version_by_name(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelByName")],
            json={"data": {"model": [{"id": 1}]}},
        )

        variant = self.test_client.model_version_by_name(
            model_class="ccfraud", model_name="variant-1"
        )

        self.assertEqual(1, variant.id())
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_deployment_by_name(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("DeploymentByName")],
            json={"data": {"deployment": [{"id": 1}]}},
        )

        deployment = self.test_client.deployment_by_name(
            deployment_name="ccfraud-deployment-1"
        )

        self.assertEqual(1, deployment.id())
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    @mock.patch.dict(os.environ, {"MODELS_ENABLED": "false"})
    def test_upload_model_stream_with_models_disabled(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/models/upload_stream",
            status=200,
            json={"insert_models": {"returning": [{"models": [{"id": 1}]}]}},
        )

        self.add_default_workspace_responder()

        with tempfile.NamedTemporaryFile() as f:
            f.write(b"model_data")

            # Are we sanitizing inputs?
            try:
                variant = self.test_client.upload_model("hello world", f.name)
            except InvalidNameError as e:
                pass
            else:
                self.assert_(False)

            # Correct case
            variant = self.test_client.upload_model("foo", f.name)

        self.assertEqual(1, variant.id())
        self.assertEqual(2, len(responses.calls))

    @responses.activate
    @mock.patch.dict(os.environ, {"MODELS_ENABLED": "true"})
    def test_upload_model_stream(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/models/upload",
            status=200,
            json={"insert_models": {"returning": [{"models": [{"id": 1}]}]}},
        )

        self.add_default_workspace_responder()
        self.add_get_configured_model()

        with tempfile.NamedTemporaryFile() as f:
            f.write(b"model_data")

            # Are we sanitizing inputs?
            try:
                variant = self.test_client.upload_model(
                    "hello world", f.name, Framework.PYTHON
                )
            except InvalidNameError as e:
                pass
            else:
                self.assert_(False)

            # Correct case
            variant = self.test_client.upload_model("foo", f.name, Framework.PYTHON)

        self.assertEqual(1, variant.id())
        self.assertEqual(3, len(responses.calls))

    def add_get_configured_model(self, status: str = "ready"):
        resp = responses.Response(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/models/get_version_by_id",
            status=200,
            json={
                "model_version": {
                    "model_version": {
                        "name": "new-model",
                        "visibility": "private",
                        "workspace_id": 1,
                        "conversion": {
                            "python_version": "3.8",
                            "requirements": [],
                            "framework": "keras",
                        },
                        "id": 1,
                        "image_path": None,
                        "input_schema": None,
                        "output_schema": None,
                        "status": status,
                        "task_id": "7f05c403-dcf4-4ecb-b5ea-28f27aa7eb7b",
                        "file_info": {
                            "version": "ec1ab8e3-923b-40dd-9f77-f20bbe8058b3",
                            "sha": "f7e49538e38bebe066ce8df97bac8be239ae8c7d2733e500c8cd633706ae95a8",
                            "file_name": "simple_model.h5",
                        },
                    },
                    "config": {
                        "id": 1,
                        "model_version_id": 1,
                        "runtime": "mlflow",
                        "input_schema": "/////Base64EncodedInputSchema=",
                        "output_schema": "/////Base64EncodedOutputSchema=",
                    },
                }
            },
        )
        responses.add(resp)
        return resp

    @responses.activate
    @mock.patch.dict(os.environ, {"MODELS_ENABLED": "true"})
    def test_upload_model_and_wait_for_convert(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/models/upload_and_convert",
            status=200,
            json={"insert_models": {"returning": [{"models": [{"id": 1}]}]}},
        )
        self.add_get_configured_model()
        self.add_default_workspace_responder()

        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelById")],
            json={
                "data": {
                    "model_by_pk": {
                        "id": 1,
                        "sha": "adsfadsf",
                        "model_id": "some_model_name",
                        "model_version": "some_model_variant_name",
                        "status": "ready",
                        "file_name": "some_model_file.onnx",
                        "updated_at": self.now.isoformat(),
                        "visibility": "private",
                    },
                },
            },
        )

        with tempfile.NamedTemporaryFile() as f:
            f.write(b"model_data")

            variant = self.test_client.upload_model(
                name="foo",
                path=f.name,
                framework=Framework.KERAS,
                convert_wait=True,
                input_schema=pa.schema([]),
                output_schema=pa.schema([]),
            )

        self.assertEqual(1, variant.id())
        self.assertEqual("ready", variant.status())
        self.assertEqual(5, len(responses.calls))

    @responses.activate
    @mock.patch.dict(os.environ, {"MODELS_ENABLED": "true"})
    def test_upload_model_and_wait_for_convert_timedout(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/models/upload_and_convert",
            status=200,
            json={"insert_models": {"returning": [{"models": [{"id": 1}]}]}},
        )
        self.add_get_configured_model("pendingconversion")
        self.add_default_workspace_responder()
        wallaroo.client.DEFAULT_MODEL_CONVERSION_TIMEOUT = 0.1

        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelById")],
            json={
                "data": {
                    "model_by_pk": {
                        "id": 1,
                        "sha": "adsfadsf",
                        "model_id": "some_model_name",
                        "model_version": "some_model_variant_name",
                        "status": "pendingconversion",
                        "file_name": "some_model_file.onnx",
                        "updated_at": self.now.isoformat(),
                        "visibility": "private",
                    },
                },
            },
        )

        with tempfile.NamedTemporaryFile() as f:
            f.write(b"model_data")

            with self.assertRaises(ModelConversionTimeoutError):
                self.test_client.upload_model(
                    name="foo",
                    path=f.name,
                    framework=Framework.KERAS,
                    convert_wait=True,
                    input_schema=pa.schema([]),
                    output_schema=pa.schema([]),
                )

        self.assertEqual(4, len(responses.calls))

    @responses.activate
    @mock.patch.dict(os.environ, {"MODELS_ENABLED": "true"})
    def test_upload_model_and_convert(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/models/upload_and_convert",
            status=200,
            json={"insert_models": {"returning": [{"models": [{"id": 1}]}]}},
        )
        self.add_get_configured_model()
        self.add_default_workspace_responder()

        with tempfile.NamedTemporaryFile() as f:
            f.write(b"model_data")

            try:
                variant = self.test_client.upload_model(
                    name="hello world",
                    path=f.name,
                    framework=Framework.KERAS,
                    convert_wait=False,
                    input_schema=pa.schema([]),
                    output_schema=pa.schema([]),
                )
            except InvalidNameError as e:
                pass
            else:
                self.assert_(False)

            # Correct case
            variant = self.test_client.upload_model(
                name="foo",
                path=f.name,
                framework=Framework.KERAS,
                convert_wait=False,
                input_schema=pa.schema([]),
                output_schema=pa.schema([]),
            )

        self.assertEqual(1, variant.id())
        self.assertEqual(3, len(responses.calls))

    @responses.activate
    @mock.patch.dict(os.environ, {"MODELS_ENABLED": "true"})
    def test_register_mlflow_model(self):
        upload_resp = responses.Response(
            method=responses.POST,
            url=f"{self.test_client.api_endpoint}/v1/api/models/upload",
            status=200,
            json={"insert_models": {"returning": [{"models": [{"id": 1}]}]}},
        )
        responses.add(upload_resp)
        get_configured_resp = self.add_get_configured_model()
        udw_resp = self.add_default_workspace_responder()
        configure_resp = add_insert_model_config_response()

        input_schema = pa.schema([pa.field("input", pa.list_(pa.float32(), 1))])
        output_schema = pa.schema([pa.field("output", pa.list_(pa.float32(), 1))])
        variant = self.test_client.register_model_image(
            "mlflow-model", "my-image"
        ).configure(
            "mlflow",
            input_schema=input_schema,
            output_schema=output_schema,
        )
        self.assertEqual(1, variant.id())
        self.assertEqual(4, len(responses.calls))
        self.assertEqual(1, upload_resp.call_count)
        self.assertEqual(1, udw_resp.call_count)
        self.assertEqual(1, get_configured_resp.call_count)
        self.assertEqual(1, configure_resp.call_count)
        upload_call = responses.calls[1]
        self.assertTrue(
            b'Content-Disposition: form-data; name="metadata"\r\nContent-Type: application/json\r\n\r\n'
            in upload_call.request.body
        )

    @responses.activate
    def test_pipelines_by_name(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineByName")],
            json={"data": {"pipeline": [{"id": 1}, {"id": 2}]}},
        )

        pipelines = self.test_client.pipelines_by_name(pipeline_name="pipeline-1")

        self.assertEqual(2, len(pipelines))
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_list_pipelines_none(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ListPipelines")],
            json={"data": {"pipeline": []}},
        )

        pipelines = self.test_client.list_pipelines()
        assert pipelines == []
        assert pipelines._repr_html_() == "(no pipelines)"

    @responses.activate
    def test_list_pipelines(self):
        self.add_deployment_for_pipeline_responder()
        self.add_list_pipeline_responder()
        self.add_pipeline_by_id_responder()
        self.add_pipeline_models_responder()
        self.add_pipeline_variant_by_id_responder()

        pipelines = self.test_client.list_pipelines()

        self.assertEqual(2, len(pipelines))
        self.assertEqual(1, len(responses.calls))

        html = pipelines._repr_html_()
        assert "<table>" in html

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_build_pipeline(self, respx_mock):
        created_pipeline_pk_id = 1
        pipeline_creation_resp = {
            "pipeline_pk_id": created_pipeline_pk_id,
            "pipeline_variant_pk_id": 1,
            "pipeline_variant_version": 1,
        }
        respx_mock.post(
            f"{self.test_client.api_endpoint}/v1/api/pipelines/create"
        ).mock(return_value=httpx.Response(200, json=pipeline_creation_resp))
        add_get_model_config_response(self.test_client.api_endpoint)
        self.add_default_workspace_responder()

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("CreatePipeline")],
            json={
                "data": {
                    "insert_pipeline": {
                        "returning": [
                            {
                                "id": 1,
                            }
                        ]
                    }
                }
            },
        )

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineById")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "id": 1,
                        "pipeline_id": "foo-278333879",
                        "created_at": "2022-02-01T18:42:27.592326+00:00",
                        "updated_at": "2022-02-01T18:42:34.055532+00:00",
                        "visibility": "private",
                        "pipeline_versions": [{"id": 2}, {"id": 1}],
                    }
                }
            },
        )

        default_model = wallaroo.model_version.ModelVersion(
            self.test_client,
            data={
                "id": 1,
                "model_id": "ccfraud",
                "model_version": "default",
                "sha": "default_sha",
            },
        )
        experiment_model = wallaroo.model_version.ModelVersion(
            self.test_client,
            data={
                "id": 2,
                "model_id": "ccfraud",
                "model_version": "experiment",
                "sha": "experiment_sha",
            },
        )
        b = self.test_client.build_pipeline(
            "vse-pipeline",
        )
        b = b.add_key_split(default_model, "card_type", {"gold": experiment_model})
        pipeline = b._upload()

        self.assertEqual(created_pipeline_pk_id, pipeline.id())
        self.assertEqual(4, len(responses.calls))

        # Are we sanitizing inputs?
        try:
            variant = self.test_client.build_pipeline("not.quite.valid")
        except InvalidNameError as e:
            pass
        else:
            self.assert_(False)

    @responses.activate
    def test_list_users(self):
        self.add_user_responder()
        users = self.test_client.list_users()

        self.assertEqual(2, len(users))
        self.assertEqual(1, len(responses.calls))
        self.assertIsInstance(users[0], User)
        self.assertIsInstance(users[1], User)
        self.assertEqual(users[0].id(), "a6fa51c3-532b-410a-a5b2-c79277f90e45")
        self.assertEqual(users[0].username(), "ci")
        self.assertEqual(users[0].email(), "ci@x.com")

    def test_generate_model_query_with_all_params(self):
        expected_query = """
            query GetModels($search_term: String!, $user_id: String!, $start_created_at: timestamptz!, $end_created_at: timestamptz!) {
              search_models(args: {search: $search_term}, where: {_and: { owner_id: {_eq: $user_id}, created_at: {_gte: $start_created_at, _lte: $end_created_at} }}, order_by: {created_at: desc}) {
                id
              }
            }
        """
        expected_params = {
            "search_term": "model",
            "user_id": "5905c14f-c70d-4afb-a1ec-8fa69e8e5f35",
            "start_created_at": self.now,
            "end_created_at": self.now,
        }

        client = self.test_client
        (query, params) = client._generate_model_query(
            user_id="5905c14f-c70d-4afb-a1ec-8fa69e8e5f35",
            search_term="model",
            start=self.now,
            end=self.now,
        )
        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_model_query_with_no_start(self):
        expected_query = """
            query GetModels($search_term: String!, $user_id: String!, $end_created_at: timestamptz!) {
              search_models(args: {search: $search_term}, where: {_and: { owner_id: {_eq: $user_id}, created_at: {_lte: $end_created_at} }}, order_by: {created_at: desc}) {
                id
              }
            }
        """
        expected_params = {
            "search_term": "model",
            "user_id": "5905c14f-c70d-4afb-a1ec-8fa69e8e5f35",
            "end_created_at": self.now,
        }

        client = self.test_client
        (query, params) = client._generate_model_query(
            user_id="5905c14f-c70d-4afb-a1ec-8fa69e8e5f35",
            search_term="model",
            end=self.now,
        )
        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_model_query_with_no_end(self):
        expected_query = """
            query GetModels($search_term: String!, $user_id: String!, $start_created_at: timestamptz!) {
              search_models(args: {search: $search_term}, where: {_and: { owner_id: {_eq: $user_id}, created_at: {_gte: $start_created_at} }}, order_by: {created_at: desc}) {
                id
              }
            }
        """
        expected_params = {
            "search_term": "model",
            "user_id": "5905c14f-c70d-4afb-a1ec-8fa69e8e5f35",
            "start_created_at": self.now,
        }

        client = self.test_client
        (query, params) = client._generate_model_query(
            user_id="5905c14f-c70d-4afb-a1ec-8fa69e8e5f35",
            search_term="model",
            start=self.now,
        )
        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_model_query_with_no_params(self):
        expected_query = """
            query GetModels($search_term: String!) {
              search_models(args: {search: $search_term}, order_by: {created_at: desc}) {
                id
              }
            }
        """
        expected_params = {"search_term": ""}
        client = self.test_client
        (query, params) = client._generate_model_query()
        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_pipelines_query_with_no_params(self):
        expected_query = f"""
            query GetPipelines($search_term: String!) {{
                search_pipelines(args: {{search: $search_term}}, distinct_on: id, order_by: {{id: desc}}) {{
                    id
                    created_at
                    pipeline_pk_id
                    updated_at
                    version
                    pipeline {{
                        id
                        pipeline_id
                        pipeline_tags {{
                            id
                            tag {{
                                id
                                tag
                            }}
                        }}
                    }}
                }}
            }}
        """

        expected_params = {"search_term": ""}
        client = self.test_client
        (query, params) = client._generate_search_pipeline_query()

        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_pipelines_query_with_user(self):
        expected_query = f"""
            query GetPipelines($search_term: String!, $user_id: String!) {{
                search_pipelines(args: {{search: $search_term}}, distinct_on: id, where: {{owner_id: {{_eq: $user_id}}}}, order_by: {{id: desc}}) {{
                    id
                    created_at
                    pipeline_pk_id
                    updated_at
                    version
                    pipeline {{
                        id
                        pipeline_id
                        pipeline_tags {{
                            id
                            tag {{
                                id
                                tag
                            }}
                        }}
                    }}
                }}
            }}
        """
        expected_params = {"search_term": "", "user_id": "my_id"}
        client = self.test_client
        (query, params) = client._generate_search_pipeline_query(user_id="my_id")

        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_pipelines_query_with_deployed(self):
        expected_query = f"""
            query GetPipelines($search_term: String!, $user_id: String!, $deployed: Boolean) {{
                search_pipelines(args: {{search: $search_term}}, distinct_on: id, where: {{_and: {{ owner_id: {{_eq: $user_id}}, pipeline: {{deployment: {{deployed: {{_eq: $deployed}}}}}} }}}}, order_by: {{id: desc}}) {{
                    id
                    created_at
                    pipeline_pk_id
                    updated_at
                    version
                    pipeline {{
                        id
                        pipeline_id
                        pipeline_tags {{
                            id
                            tag {{
                                id
                                tag
                            }}
                        }}
                    }}
                }}
            }}
        """
        expected_params = {"search_term": "", "user_id": "my_id", "deployed": True}
        client = self.test_client
        (query, params) = client._generate_search_pipeline_query(
            user_id="my_id", deployed=True
        )

        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_pipelines_query_with_created_at(self):
        expected_query = f"""
            query GetPipelines($search_term: String!, $user_id: String!, $start_created_at: timestamptz!) {{
                search_pipelines(args: {{search: $search_term}}, distinct_on: id, where: {{_and: {{ owner_id: {{_eq: $user_id}}, created_at: {{_gte: $start_created_at}} }}}}, order_by: {{id: desc}}) {{
                    id
                    created_at
                    pipeline_pk_id
                    updated_at
                    version
                    pipeline {{
                        id
                        pipeline_id
                        pipeline_tags {{
                            id
                            tag {{
                                id
                                tag
                            }}
                        }}
                    }}
                }}
            }}
        """
        expected_params = {
            "search_term": "",
            "user_id": "my_id",
            "start_created_at": self.now,
        }
        client = self.test_client
        (query, params) = client._generate_search_pipeline_query(
            user_id="my_id", created_start=self.now
        )

        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_generate_pipelines_query_with_updated_at(self):
        expected_query = f"""
            query GetPipelines($search_term: String!, $user_id: String!, $start_created_at: timestamptz!, $start_updated_at: timestamptz!, $end_updated_at: timestamptz!) {{
                search_pipelines(args: {{search: $search_term}}, distinct_on: id, where: {{_and: {{ owner_id: {{_eq: $user_id}}, created_at: {{_gte: $start_created_at}}, updated_at: {{_gte: $start_updated_at, _lte: $end_updated_at}} }}}}, order_by: {{id: desc}}) {{
                    id
                    created_at
                    pipeline_pk_id
                    updated_at
                    version
                    pipeline {{
                        id
                        pipeline_id
                        pipeline_tags {{
                            id
                            tag {{
                                id
                                tag
                            }}
                        }}
                    }}
                }}
            }}
        """
        expected_params = {
            "search_term": "",
            "user_id": "my_id",
            "start_created_at": self.now,
            "start_updated_at": self.now,
            "end_updated_at": self.now,
        }
        client = self.test_client
        (query, params) = client._generate_search_pipeline_query(
            user_id="my_id",
            created_start=self.now,
            updated_start=self.now,
            updated_end=self.now,
        )

        assert expected_query.translate(string.whitespace) == query.translate(
            string.whitespace
        )
        assert expected_params == params

    def test_jupyter_client(self):
        with patch.dict("os.environ", {"JUPYTER_SVC_SERVICE_HOST": "x://yz"}):
            client = wallaroo.Client(auth_type="test_auth")
            assert client._interactive == True

            client = wallaroo.Client(interactive=True, auth_type="test_auth")
            assert client._interactive == True

            client = wallaroo.Client(interactive=False, auth_type="test_auth")
            assert client._interactive == False

    def test_non_jupyter_client(self):
        mockenv = os.environ
        if "JUPYTER_SVC_SERVICE_HOST" in mockenv:
            del mockenv["JUPYTER_SVC_SERVICE_HOST"]

        with patch.dict("os.environ", mockenv):
            client = self.test_client
            assert client._interactive == False

            client = wallaroo.Client(interactive=True, auth_type="test_auth")
            assert client._interactive == True

            client = wallaroo.Client(interactive=False, auth_type="test_auth")
            assert client._interactive == False

    @responses.activate
    def test_search_pipelines_none(self):
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("GetPipelines")],
            json={"data": {"search_pipelines": []}},
        )

        result = self.test_client.search_pipeline_versions()
        assert result == []
        assert result._repr_html_() == "(no pipelines)"

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_list_assays_none(self, respx_mock):
        respx_mock.post(f"{self.test_client.api_endpoint}/v1/api/assays/list").mock(
            return_value=httpx.Response(200, json=[])
        )

        assays = self.test_client.list_assays()
        assert assays == []
        assert assays._repr_html_() == "(no assays)"

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_list_assays(self, respx_mock):
        self.add_list_assays_responder(respx_mock)
        assays = self.test_client.list_assays()

        self.assertEqual(2, len(assays))
        self.assertEqual("mypipeline", assays[1]._pipeline_name)
        html = assays._repr_html_()
        assert "</table>" in html
        assert "<td>mypipeline</td>" in html

    @respx.mock(assert_all_mocked=True)
    def test_get_assay_results(self, respx_mock):
        resp = respx_mock.post("http://api-lb:8080/v1/api/assays/get_assay_results").mock(
            return_value=httpx.Response(200, json=SAMPLE_GET_ASSAYS_RESULTS)
        )
        #naive dates
        start_date = datetime(2023, 10, 11, 0, 0, 0, 0)
        end_date = datetime(2023, 10, 13, 0, 0, 0, 0)

        # tz aware dates
        start_date_utc = start_date.astimezone(tz=timezone.utc)
        end_date_utc = end_date.astimezone(tz=timezone.utc)

        assay_results = self.test_client.get_assay_results(assay_id=27, start=start_date, end=end_date)

        # Check that the request was made with the correct parameters - verify dates are tz aware
        response_params = json.loads(resp.calls.last.request.content.decode('utf8'))
        self.assertDictEqual({'assay_id': 27, 'start': start_date_utc.isoformat(), 'end': end_date_utc.isoformat()}, response_params)

        # Check that the response was parsed correctly
        self.assertEqual(len(assay_results), 2)
        self.assertEqual(assay_results[0].assay_id, 27)


@responses.activate
@respx.mock(assert_all_mocked=True)
def test_build_assay(respx_mock):
    class Pipeline:
        def id(self):
            return 0

        def name(self):
            return "pipy"

    resp = respx_mock.post("http://api-lb:8080/v1/api/assays/summarize", ).mock(
        return_value=httpx.Response(200, json={
            "count": 188,
            "min": 11.986584663391112,
            "max": 14.29722023010254,
            "mean": 13.031112508570894,
            "median": 12.956134796142578,
            "std": 0.4770556767131347,
            "edges": [11.986584663391112, 12.622478485107422, 12.854415893554688, 13.064453125, 13.440485000610352,
                      14.29722023010254, None],
            "edge_names": ["left_outlier", "q_20", "q_40", "q_60", "q_80", "q_100", "right_outlier"],
            "aggregated_values": [0.0, 0.20212765957446807, 0.19680851063829788, 0.20212765957446807,
                                  0.19680851063829788, 0.20212765957446807, 0.0],
            "aggregation": "Density",
            "start": "2023-01-01T00:00:00+00:00",
            "end": "2023-01-02T00:00:00+00:00",
        })
    )
    responses.add(
        responses.POST,
        "http://api-lb:8080/v1/graphql",
        status=200,
        match=[testutil.query_name_matcher("UserDefaultWorkspace")],
        json={
            "data": {
                "user_default_workspace": [
                    {
                        "workspace": {
                            "id": 1,
                        }
                    }
                ]
            }
        },
    )

    gql_client = testutil.new_gql_client(endpoint="http://api-lb:8080/v1/graphql")
    client = wallaroo.Client(
        gql_client=gql_client,
        auth_endpoint="http://mock-keycloak:1234",
        auth_type="test_auth",
    )

    p = Pipeline()
    a = client.build_assay(
        "test",
        cast(wallaroo.pipeline.Pipeline, p),
        "model_name",
        "output 0 0",
        datetime.now(),
        datetime.now(),
    )
    ad = json.loads(a.build().to_json())
    assert ad["name"] == "test"
