import datetime
import responses
import unittest
import respx

import wallaroo
from wallaroo import functions as fn
from wallaroo.deployment import WaitForDeployError
from wallaroo.model_version import ModelVersion
from wallaroo.model_config import ModelConfig
from wallaroo.pipeline import Pipeline
from wallaroo.pipeline_version import PipelineVersion

from . import status_samples
from . import testutil
from unit_tests.reusable_responders import (
    add_create_pipeline_responder,
    add_deploy_responder, add_insert_model_config_response,
)


class TestPipelineVersion(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client, request_timeout=2, auth_type="test_auth"
        )

    @responses.activate
    def test_init_full_dict(self):
        variant = PipelineVersion(
            client=self.test_client,
            data={
                "id": 2,
                "version": "v1",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "definition": {
                    "id": "test-pipeline",
                    "steps": [
                        {
                            "id": "metavalue_split",
                            "args": ["card_type", "default", "gold", "experiment"],
                            "operation": "map",
                        }
                    ],
                },
                "pipeline": {"id": 1},
                "deployment_pipeline_versions": [],
            },
        )

        self.assertEqual(2, variant.id())
        self.assertEqual("v1", variant.name())
        self.assertEqual(self.now, variant.create_time())
        self.assertEqual(self.now, variant.last_update_time())
        self.assertEqual(
            {
                "id": "test-pipeline",
                "steps": [
                    {
                        "id": "metavalue_split",
                        "args": ["card_type", "default", "gold", "experiment"],
                        "operation": "map",
                    }
                ],
            },
            variant.definition(),
        )
        self.assertIsInstance(variant.pipeline(), Pipeline)
        # TODO: Test deployment_pipeline_versions

    @responses.activate
    def test_rehydrate(self):
        testcases = [
            ("name", "v1"),
            ("create_time", self.now),
            ("last_update_time", self.now),
            (
                "definition",
                {
                    "id": "test-pipeline",
                    "steps": [
                        {
                            "id": "metavalue_split",
                            "args": ["card_type", "default", "gold", "experiment"],
                            "operation": "map",
                        }
                    ],
                },
            )
            # TODO: Test deployments()
        ]
        for method_name, want_value in testcases:
            with self.subTest():
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

                variant = PipelineVersion(client=self.test_client, data={"id": 2})

                self.assertEqual(want_value, getattr(variant, method_name)())
                self.assertEqual(1, len(responses.calls))
                # Another call to the same accessor shouldn't trigger any
                # additional GraphQL queries.
                self.assertEqual(want_value, getattr(variant, method_name)())
                self.assertEqual(1, len(responses.calls))
                responses.reset()

    @responses.activate
    @respx.mock(assert_all_called=True)
    def test_deploy(self, respx_mock):
        workspace_name = "test-logs-workspace"

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
                                "archived": False,
                                "created_at": "2022-02-15T09:42:12.857637+00:00",
                                "created_by": "bb2dec32-09a1-40fd-8b34-18bd61c9c070",
                                "name": f"{workspace_name}",
                                "id": 1,
                                "pipelines": [],
                                "models": [],
                            }
                        }
                    ]
                }
            },
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
        # ids will be wrong for one of the model config calls, but we're only checking runtime
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
                            "id": 1,
                        },
                        "runtime": "onnx",
                        "tensor_fields": None,
                    },
                },
            },
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("DeploymentById")],
            json={
                "data": {
                    "deployment_by_pk": {
                        "id": 10,
                        "deploy_id": "foo-deployment",
                        "deployed": False,
                        "engine_config": {
                            "engine": {},
                        },
                    },
                },
            },
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelById")],
            json={
                "data": {
                    "model_by_pk": {
                        "id": 1,
                        "arch": None,
                    },
                },
            },
        )
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "foo-deployment-10"})],
            status=200,
            json=status_samples.RUNNING,
        )

        add_deploy_responder(respx_mock, 10, self.test_client.api_endpoint)

        default_model_config = ModelConfig(
            self.test_client,
            data={
                "id": 1,
                "model": {"id": 1, "model_id": "ccfraud", "model_version": "default"},
            },
        )
        experiment_model_config = ModelConfig(
            self.test_client,
            data={
                "id": 2,
                "model": {
                    "id": 2,
                    "model_id": "ccfraud",
                    "model_version": "experiment",
                },
            },
        )
        variant = PipelineVersion(
            client=self.test_client,
            data={
                "id": 1,
            },
        )

        deployment = variant.deploy(
            "foo-deployment", [default_model_config, experiment_model_config]
        )

        self.assertEqual(8, len(responses.calls))
        self.assertEqual(10, deployment.id())
        self.assertEqual("foo-deployment", deployment.name())

        # redo with failure case
        responses.replace(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "foo-deployment-10"})],
            status=200,
            json=status_samples.ERROR,
        )

        with self.assertRaises(WaitForDeployError):
            deployment = variant.deploy(
                "foo-deployment", [default_model_config, experiment_model_config]
            )

    @responses.activate
    @respx.mock(assert_all_called=True)
    def test_alert_configuration(self, respx_mock):
        add_create_pipeline_responder(
            respx_mock, 1, api_endpoint=self.test_client.api_endpoint
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
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("CreateAlertConfiguration")],
            json={"data": {}},
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelById")],
            json={
                "data": {
                    "model_by_pk": {
                        "id": 1,
                        "sha": "asdfads",
                        "model_id": "some_model_name",
                        "model_version": "some_model_variant_name",
                        "file_name": "some_model_file.onnx",
                        "updated_at": self.now.isoformat(),
                        "visibility": "private",
                    },
                },
            },
        )
        add_insert_model_config_response(self.test_client.api_endpoint)

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

        default_model = ModelVersion(
            self.test_client,
            data={
                "id": 1,
                "model_id": "ccfraud",
                "model_version": "default",
                "sha": "ccfraud_sha",
            },
        )

        pipeline = self.test_client.build_pipeline(
            "vse-pipeline",
        )
        pipeline.add_model_step(default_model)
        pipeline.add_alert(
            "high_fraud",
            fn.count(default_model.config().inputs[0][0] > 0.95, "1h") > 10,
            [],
        )
        pipeline = pipeline._upload()

        self.assertEqual(5, len(responses.calls))
