from wallaroo.object import InvalidNameError
import wallaroo
from wallaroo.deployment import WaitForDeployError
from wallaroo.pipeline import Pipeline
from wallaroo.model_version import ModelVersion
from wallaroo.tag import Tag

import datetime
from io import StringIO
import os
import responses
import time
import unittest
from unittest import mock
from unittest.mock import patch
import respx

from . import status_samples
from . import testutil
from .reusable_responders import (
    add_deploy_responder,
    add_create_pipeline_responder,
    add_undeploy_responder,
    add_insert_model_config_response,
    add_get_model_config_response
)


class TestModelVersion(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client,
            request_timeout=2,
            interactive=False,
            auth_type="test_auth",
        )

    def add_deploy_onnx_responses(self, respx_mock):
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("WorkspaceById")],
            json={
                "data": {
                    "workspace_by_pk": {
                        "id": 1,
                        "name": "Unused workspace name",
                        "created_at": self.now.isoformat(),
                        "created_by": 44,
                        "pipelines": [],
                        "models": [],
                        "users": [],
                        "archived": False,
                    }
                },
            },
        )

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("ConfigureModel")],
            json={
                "data": {
                    "insert_model_config": {
                        "returning": [
                            {
                                "id": 2,
                            }
                        ]
                    }
                }
            },
        )

        add_deploy_responder(respx_mock, 3, self.test_client.api_endpoint)

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("DeploymentById")],
            json={
                "data": {
                    "deployment_by_pk": {
                        "id": 3,
                        "deploy_id": "my-deployment-name",
                        "deployed": False,
                        "deployment_model_configs": [
                            {
                                "model_config": {
                                    "id": 3,
                                },
                            },
                        ],
                    },
                },
            },
        )

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
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
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "my-deployment-name-3"})],
            status=200,
            json=status_samples.RUNNING,
        )

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelConfigById")],
            json={
                "data": {
                    "model_config_by_pk": {
                        "id": 1,
                        "filter_threshold": 0.1234,
                        "model": {
                            "id": 2,
                        },
                        "runtime": "onnx",
                        "tensor_fields": None,
                    },
                },
            },
        )

        # FIXME TODO OPTIMIZE - This one is because we are deploying a model we already have in
        # hand but it's going out to server anyway. This could be short circuited.
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelById")],
            json={
                "data": {
                    "model_by_pk": {
                        "id": 1,
                        "sha": "adfaf",
                        "model_id": "some_model_name",
                        "model_version": "some_model_variant_name",
                        "file_name": "some_model_file.onnx",
                        "updated_at": self.now.isoformat(),
                        "visibility": "private",
                        "arch": None,
                    },
                },
            },
        )

        # FIXME TODO OPTIMIZE - This one is because we are deploying a model we already have in
        # hand but it's going out to server anyway. This could be short circuited.
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("InsertDeploymentModelConfig")],
            json={"data": {}},  # Return data currently unused
        )

        # FIXME TODO OPTIMIZE - This one is because we are deploying a model we already have in
        # hand but it's going out to server anyway. This could be short circuited.
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("InsertDeploymentPipelineVersion")],
            json={"data": {}},  # Return data currently unused
        )

        # TODO same ...
        add_create_pipeline_responder(
            respx_mock, api_endpoint=self.test_client.api_endpoint
        )

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineVariantById")],
            json={
                "data": {
                    "pipeline_version_by_pk": {
                        "id": 2,
                        "created_at": self.now.isoformat(),
                        "updated_at": self.now.isoformat(),
                        "version": "v1",
                        "pipeline": {"id": 1},
                        "deployment_pipeline_versions": [],
                    }
                }
            },
        )

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
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

        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "my-deployment-name-3"})],
            status=200,
            json=status_samples.RUNNING,
        )

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("QueryLimitStatus")],
            json={"data": {"deployment": []}},
        )

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("Undeploy")],
            json={"data": {}},  # Return data currently unused
        )

    def create_onnx_model(self, client):
        return ModelVersion(
            client=client,
            data={
                "id": 1,
                "model_id": "some_model_name",
                "model_version": "some_model_variant_name",
                "file_name": "some_model_file.onnx",
                "updated_at": self.now.isoformat(),
                "visibility": "private",
            },
        )

    @responses.activate
    def test_init_full_dict(self):
        variant = ModelVersion(
            client=self.test_client,
            data={
                "id": 1,
                "model_id": "some_model_name",
                "model_version": "some_model_variant_name",
                "file_name": "some_model_file.onnx",
                "updated_at": self.now.isoformat(),
                "visibility": "private",
            },
        )

        self.assertEqual(1, variant.id())
        self.assertEqual("some_model_variant_name", variant.version())
        self.assertEqual("some_model_name", variant.name())
        self.assertEqual("some_model_file.onnx", variant.file_name())
        self.assertEqual(self.now, variant.last_update_time())

    @responses.activate
    def test_rehydrate(self):
        testcases = [
            ("name", "some_model_name"),
            ("version", "some_model_variant_name"),
            ("status", "ready"),
            ("file_name", "some_model_file.onnx"),
            ("last_update_time", self.now),
        ]
        for method_name, want_value in testcases:
            with self.subTest(method_name=method_name):
                responses.add(
                    responses.POST,
                    "http://api-lb/v1/graphql",
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

                variant = ModelVersion(client=self.test_client, data={"id": 1})

                self.assertEqual(want_value, getattr(variant, method_name)())
                if method_name == "status":
                    self.assertEqual(2, len(responses.calls))
                else:
                    self.assertEqual(1, len(responses.calls))
                responses.reset()

    @responses.activate
    @mock.patch.dict(os.environ, {"MODELS_ENABLED": "false"})
    def test_configure_with_models_ff_disabled(self):
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("ConfigureModel")],
            json={
                "data": {
                    "insert_model_config": {
                        "returning": [
                            {
                                "id": 2,
                            }
                        ]
                    }
                }
            },
        )

        model = ModelVersion(
            client=self.test_client,
            data={
                "id": 1,
                "model_id": "some_model_name",
                "model_version": "some_model_variant_name",
                "file_name": "some_model_file.onnx",
                "updated_at": self.now.isoformat(),
                "visibility": "private",
            },
        )
        config = model.configure(runtime="onnx")

        self.assertIsInstance(config, ModelVersion)
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    def test_configure(self):
        add_insert_model_config_response(self.test_client.api_endpoint)
        model = ModelVersion(
            client=self.test_client,
            data={
                "id": 1,
                "model_id": "some_model_name",
                "model_version": "some_model_variant_name",
                "file_name": "some_model_file.onnx",
                "updated_at": self.now.isoformat(),
                "visibility": "private",
            },
        )
        config = model.configure(runtime="onnx")

        self.assertIsInstance(config, ModelVersion)
        self.assertEqual(1, len(responses.calls))

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_deploy_onnx_noninteractive(self, respx_mock):
        self.add_deploy_onnx_responses(respx_mock)
        variant = self.create_onnx_model(self.test_client)
        add_get_model_config_response(self.test_client.api_endpoint)
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            with patch("sys.stderr", new_callable=StringIO) as stderr:
                deployment = variant.deploy("my-deployment-name")
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(stderr.getvalue(), "")

        self.assertIsInstance(deployment, Pipeline)
        self.assertEqual(10, len(responses.calls))

        # tack on a failure case
        responses.replace(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "my-deployment-name-3"})],
            status=200,
            json=status_samples.ERROR,
        )

        beg = time.time()
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            with patch("sys.stderr", new_callable=StringIO) as stderr:
                with self.assertRaises(WaitForDeployError):
                    deployment = variant.deploy("my-deployment-name")
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(stderr.getvalue(), "")

        end = time.time()
        self.assertTrue(end - beg > 2)

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_deploy_onnx_interactive(self, respx_mock):
        test_client = wallaroo.Client(
            gql_client=self.gql_client,
            request_timeout=2,
            interactive=True,
            auth_type="test_auth",
        )

        self.add_deploy_onnx_responses(respx_mock)
        variant = self.create_onnx_model(test_client)
        add_get_model_config_response(test_client.api_endpoint)

        with patch("sys.stdout", new_callable=StringIO) as stdout:
            with patch("sys.stderr", new_callable=StringIO) as stderr:
                # validate that 'deploy' requires DNS-compliant names
                try:
                    variant.deploy("not-quite-right-")
                except InvalidNameError as _:
                    pass
                else:
                    assert False
                deployment = variant.deploy("my-deployment-name")
                self.assertEqual(stdout.getvalue(), " ok\n")
                self.assertEqual(stderr.getvalue(), "")

        self.assertIsInstance(deployment, Pipeline)
        self.assertEqual(10, len(responses.calls))

        # tack on a failure case
        responses.replace(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "my-deployment-name-3"})],
            status=200,
            json=status_samples.ERROR,
        )

        beg = time.time()
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            with patch("sys.stderr", new_callable=StringIO) as stderr:
                with self.assertRaises(WaitForDeployError):
                    deployment = variant.deploy("my-deployment-name")
                self.assertTrue(stdout.getvalue().startswith("Waiting for deployment"))
                self.assertEqual(stderr.getvalue(), "")

        end = time.time()
        self.assertTrue(end - beg > 2)

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_undeploy_onnx_interactive(self, respx_mock):
        test_client = wallaroo.Client(
            gql_client=self.gql_client,
            request_timeout=2,
            interactive=True,
            auth_type="test_auth",
        )

        self.add_deploy_onnx_responses(respx_mock)
        add_undeploy_responder(respx_mock, self.test_client.api_endpoint)
        variant = self.create_onnx_model(test_client)
        add_get_model_config_response(test_client.api_endpoint)

        # get a normal deployment
        success_deployment = variant.deploy("my-deployment-name")
        self.assertIsInstance(success_deployment, Pipeline)
        self.assertEqual(10, len(responses.calls))

        # failure case
        beg = time.time()
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            with patch("sys.stderr", new_callable=StringIO) as stderr:
                with self.assertRaises(RuntimeError):
                    deployment = success_deployment.undeploy()
                self.assertTrue(
                    stdout.getvalue().startswith("Waiting for undeployment")
                )
                self.assertEqual(stderr.getvalue(), "")

        end = time.time()
        self.assertTrue(end - beg > 2)

        # success case
        responses.replace(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "my-deployment-name-3"})],
            status=404,
        )
        with patch("sys.stdout", new_callable=StringIO) as stdout:
            with patch("sys.stderr", new_callable=StringIO) as stderr:
                success_deployment.undeploy()
                outvalue = stdout.getvalue()
                self.assertEqual(stdout.getvalue(), " ok\n")
                self.assertEqual(stderr.getvalue(), "")

    @responses.activate
    @mock.patch.dict(os.environ, {"ARROW_ENABLED": "false"})
    def test_logs(self):
        responses.add(
            responses.GET,
            f"{self.test_client.api_endpoint}/v1/logs/topic/model-x-inference",
            status=200,
            json={
                "partitions": {
                    "testing-1": {"start": 0, "end": 20},
                    "testing-2": {"start": 0, "end": 2},
                }
            },
        )

        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/logs/topic/model-x-inference/records",
            status=200,
            json={
                "records": [
                    '{"model_name":"x","model_version":"0002","pipeline_id":"","outputs":[{"Float":{"v":1,"dim":[1,1],"data":[-0.000041961669921875]}}],"elapsed":43059,"time":1642193935934,"original_data":{"tensor":[[0.0]]},"check_failures":[]}'
                ]
            },
            match=[responses.matchers.json_params_matcher({"testing-1": 10, "testing-2": 0})],
        )

        variant = ModelVersion(
            client=self.test_client,
            data={
                "id": 1,
                "model_id": "x",
                "model_version": "some_model_variant_name",
                "file_name": "some_model_file.onnx",
                "updated_at": self.now.isoformat(),
                "visibility": "private",
            },
        )

        self.assertEqual(len(variant.logs(20)), 1)

    @responses.activate
    def test_pipeline_tags(self):
        tag_1 = Tag(client=self.test_client, data={"id": 1, "tag": "bartag314"})
        tag_2 = Tag(client=self.test_client, data={"id": 2, "tag": "footag123"})

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelById")],
            json={
                "data": {
                    "model_by_pk": {
                        "id": 1,
                        "sha": "adsfadsf",
                        "model_id": "some_model_name",
                        "model_version": "some_model_variant_name",
                        "file_name": "some_model_file.onnx",
                        "updated_at": self.now.isoformat(),
                        "visibility": "private",
                        "model_tags": [
                            {"tag": {"id": 1, "tag": "bartag314"}},
                            {"tag": {"id": 2, "tag": "footag123"}},
                        ],
                    },
                },
            },
        )

        variant = ModelVersion(client=self.test_client, data={"id": 1})
        self.assertListEqual(
            list(map(vars, [tag_1, tag_2])), list(map(vars, variant.tags()))
        )
