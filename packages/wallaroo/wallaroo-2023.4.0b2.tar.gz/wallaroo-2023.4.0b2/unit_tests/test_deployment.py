import datetime
import httpx
import json
import os
import respx
import tempfile
import time
import unittest
from unittest import mock
import pandas as pd
import pyarrow as pa
import responses
import numpy

import wallaroo
from wallaroo.deployment import (
    Deployment,
    WaitForDeployError,
    hack_pandas_dataframe_order,
)
from wallaroo.model_config import ModelConfig
from wallaroo.model_version import ModelVersion
from wallaroo.object import CommunicationError, EntityNotFoundError
from wallaroo.pipeline_version import PipelineVersion

from . import status_samples
from . import testutil
from .reusable_responders import add_insert_model_config_response

with open("unit_tests/outputs/sample_inference_result.json", "r") as fp:
    SAMPLE_INFERENCE_RESULT = json.loads(fp.read())

with open("unit_tests/outputs/sample_batched_inference_result.json", "r") as fp:
    SAMPLE_BATCHED_INFERENCE_RESULT = json.loads(fp.read())

SAMPLE_ARROW_FILE = "unit_tests/outputs/dev_smoke_test.arrow"
SAMPLE_PANDAS_RECORDS_FILE = "unit_tests/outputs/dev_smoke_test.pandas.json"
SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE = json.load(
    open('unit_tests/outputs/sample_inference_result.pandas.json', 'rb'))

sink = pa.BufferOutputStream()
with pa.ipc.open_file("unit_tests/outputs/sample_inference_result.arrow") as reader:
    infer_result_table = reader.read_all()
    with pa.ipc.new_file(sink, infer_result_table.schema) as arrow_ipc:
        arrow_ipc.write(infer_result_table)
        arrow_ipc.close()
SAMPLE_ARROW_INFERENCE_RESULT_TABLE = infer_result_table
SAMPLE_ARROW_INFERENCE_RESPONSE = sink.getvalue()
with open("unit_tests/outputs/dev_smoke_test.pandas.json", "r") as fp:
    SAMPLE_PANDAS_RECORDS_JSON = pd.read_json(fp)


class TestDeployment(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")
        self.test_client = wallaroo.Client(
            api_endpoint="http://api-lb:1234",
            gql_client=self.gql_client,
            auth_type="test_auth",
            request_timeout=2,  # this field used only by deployment.wait_for_running() tests
        )
        
        self.gql_client = testutil.new_gql_client(endpoint="http://foo.org/v1/graphql")
        self.remote_test_client = wallaroo.Client(
            api_endpoint="http://foo.api.org:1234",
            gql_client=self.gql_client,
            request_timeout=2,  # this field used only by deployment.wait_for_running() tests
        )        

    def assert_wait_for_running(self, deployment, exception_type):
        """Expects a timeout and exception type"""
        begtime = time.time()
        with self.assertRaises(exception_type):
            res = deployment.wait_for_running()
        endtime = time.time()
        elapsed = endtime - begtime
        self.assertTrue(1.0 <= elapsed <= self.test_client.timeout + 3)

    @responses.activate
    def test_init_full_dict(self):

        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some_deployment_name",
                "deployed": False,
                "deployment_model_configs": [
                    {
                        "model_config": {
                            "id": 2,
                        },
                    },
                ],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 3,
                        }
                    }
                ],
            },
        )

        self.assertEqual(1, deployment.id())
        self.assertEqual("some_deployment_name", deployment.name())
        self.assertEqual(False, deployment.deployed())
        self.assertIsInstance(deployment.model_configs()[0], ModelConfig)
        self.assertIsInstance(deployment.pipeline_versions()[0], PipelineVersion)

    @responses.activate
    def test_rehydrate(self):
        testcases = [
            ("name", "some_deployment_name"),
            ("deployed", False),
            ("model_configs", None),
            ("pipeline_versions", None),
        ]
        for method_name, want_value in testcases:
            with self.subTest():
                responses.add(
                    responses.POST,
                    "http://api-lb/v1/graphql",
                    status=200,
                    match=[testutil.query_name_matcher("DeploymentById")],
                    json={
                        "data": {
                            "deployment_by_pk": {
                                "id": 1,
                                "deploy_id": "some_deployment_name",
                                "deployed": False,
                                "deployment_model_configs": [
                                    {
                                        "model_config": {
                                            "id": 2,
                                        },
                                    },
                                ],
                                "deployment_pipeline_versions": [
                                    {
                                        "pipeline_version": {
                                            "id": 3,
                                        }
                                    }
                                ],
                            },
                        },
                    },
                )

                deployment = Deployment(client=self.test_client, data={"id": 1})
                got_value = getattr(deployment, method_name)()

                if want_value is not None:
                    self.assertEqual(want_value, got_value)
                self.assertEqual(1, len(responses.calls))
                # Another call to the same accessor shouldn't trigger any
                # additional GraphQL queries.
                got_value = getattr(deployment, method_name)()
                if want_value is not None:
                    self.assertEqual(want_value, got_value)
                self.assertEqual(1, len(responses.calls))
                responses.reset()

    @responses.activate
    @mock.patch.dict(os.environ, {"ARROW_ENABLED": "false"})
    def test_infer_on_pipeline(self):
        responses.add(
            responses.POST,
            url="http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            json=SAMPLE_INFERENCE_RESULT,
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.json_body_printer()],
        )
        input = {"tensor": [[1.0678324729342086]]}
        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
                "pipeline": {
                    "pipeline_id": "some-pipeline",
                },
            },
        )

        output = deployment.infer(input)
        self.assertEqual(
            numpy.ndarray(shape=(1, 1), buffer=numpy.array([0.1])), output[0].data()[0]
        )

        # Infer should check its tensor type
        with self.assertRaises(TypeError):
            deployment.infer(123)

        with self.assertRaises(TypeError):
            deployment.infer("foo")

        with self.assertRaises(TypeError):
            deployment.infer([])

    @responses.activate
    @mock.patch.dict(os.environ, {"ARROW_ENABLED": "false"})
    def test_infer_from_file(self):
        responses.add(
            responses.POST,
            url="http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            json=SAMPLE_INFERENCE_RESULT,
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.json_body_printer()],
        )
        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
                "pipeline": {
                    "pipeline_id": "some-pipeline",
                },
            },
        )
        with tempfile.NamedTemporaryFile(mode="w") as f:
            input = {"tensor": [[1.0678324729342086]]}
            json.dump(input, f)
            f.flush()

            output = deployment.infer_from_file(f.name)

        self.assertEqual(
            numpy.ndarray(shape=(1, 1), buffer=numpy.array([0.1])), output[0].data()
        )

        # Infer should check its tensor type. Yes these are all valid JSONs.

        with tempfile.NamedTemporaryFile(mode="w") as f:
            input = 123
            json.dump(input, f)
            f.flush()
            with self.assertRaises(TypeError):
                deployment.infer_from_file(f.name)

        with tempfile.NamedTemporaryFile(mode="w") as f:
            input = "foo"
            json.dump(input, f)
            f.flush()
            with self.assertRaises(TypeError):
                deployment.infer_from_file(f.name)

        with tempfile.NamedTemporaryFile(mode="w") as f:
            input = []
            json.dump(input, f)
            f.flush()
            with self.assertRaises(TypeError):
                deployment.infer_from_file(f.name)

    @responses.activate
    def test_infer_from_file_with_arrow(self):

        responses.add(
            responses.POST,
            url="http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            body=SAMPLE_ARROW_INFERENCE_RESPONSE,
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.json_body_printer()],
        )
        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
                "pipeline": {
                    "pipeline_id": "some-pipeline",
                },
            },
        )

        output = deployment.infer_from_file(SAMPLE_ARROW_FILE)

        self.assertIsInstance(output, pa.Table)
        output.equals(infer_result_table)

    def test_pandas_order_hack(self):
        # hacky fake aloha-like data
        columns = [
            "out.banjori",
            "out.cryptolocker",
            "out.main",
            "out.dircrypt",
            "out._model_split",
            "out.ramdo",
            "time",
            "out.suppobox",
            "out.ramnit",
            "out.corebot",
            "out.pykspa",
            "out.gozi",
            "out.matsnu",
            "in.text_input",
            "out.qakbot",
            "out.locky",
            "out.simda",
            "out.kraken",
        ]
        df = pd.DataFrame(data=[list(range(len(columns)))] * 10, columns=columns)

        fixed = hack_pandas_dataframe_order(df)

        self.assertEqual(
            list(fixed.columns)[:4],
            ["time", "in.text_input", "out._model_split", "out.banjori"],
        )

    @responses.activate
    def test_infer_from_file_with_pandas_records(self):
        result_df = pd.DataFrame.from_records(SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE)

        responses.add(
            responses.POST,
            url="http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            json=SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE,
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.json_body_printer()],
        )
        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
                "pipeline": {
                    "pipeline_id": "some-pipeline",
                },
            },
        )

        output_df = deployment.infer_from_file(SAMPLE_PANDAS_RECORDS_FILE)
        self.assertIsInstance(output_df, pd.DataFrame)
        self.assertEqual(type(output_df["time"][0]), pd.Timestamp)
        self.assertEqual(type(output_df["check_failures"][0]), numpy.int64)

    @responses.activate
    def test_infer_from_file_with_invalid_file_type(self):

        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
            },
        )
        with self.assertRaises(TypeError):
            output = deployment.infer_from_file("unit_tests/outputs/dev_smoke_test.txt")

    @responses.activate
    def test_infer_with_arrow(self):
        with pa.ipc.open_file("unit_tests/outputs/dev_smoke_test.arrow") as source:
            table = source.read_all()

        responses.add(
            responses.POST,
            url="http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            body=SAMPLE_ARROW_INFERENCE_RESPONSE,
        )

        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
                "pipeline": {
                    "pipeline_id": "some-pipeline",
                },
            },
        )

        output = deployment.infer(table)
        self.assertIsInstance(output, pa.Table)
        self.assertEqual(output["time"].type, pa.timestamp(unit="ms"))
        self.assertEqual(output["check_failures"].type, pa.int8())

        # Infer should check its tensor type
        with self.assertRaises(TypeError):
            deployment.infer(123)

        with self.assertRaises(TypeError):
            deployment.infer("foo")

    @responses.activate
    def test_infer_with_pandas_records(self):
        data_df = pd.DataFrame.from_records(SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE)

        responses.add(
            responses.POST,
            url="http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            json=SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE,
        )

        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
                "pipeline": {
                    "pipeline_id": "some-pipeline",
                },
            },
        )

        output_df = deployment.infer(SAMPLE_PANDAS_RECORDS_JSON)
        self.assertIsInstance(output_df, pd.DataFrame)
        self.assertEqual(type(output_df["time"][0]), pd.Timestamp)
        self.assertEqual(type(output_df["check_failures"][0]), numpy.int64)

        # Infer should check its tensor type
        with self.assertRaises(TypeError):
            deployment.infer(123)

        with self.assertRaises(TypeError):
            deployment.infer("foo")

    @responses.activate
    def test_replace_configured_model(self):
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("ReplaceModel")],
            json={
                "data": {
                    "insert_deployment_model_configs": {
                        "id": 1,
                        "deployment_id": 2,
                        "model_config_id": 3,
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
                        "id": 2,
                        "deploy_id": "some_deployment_name",
                        "deployed": True,
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
        mc = ModelConfig(client=self.test_client, data={"id": 3})
        d = Deployment(client=self.test_client, data={"id": 2})

        d = d.replace_configured_model(mc)

        self.assertEqual(2, d.id())
        self.assertEqual(3, d.model_configs()[0].id())

    @responses.activate
    def test_replace_model(self):
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("ModelById")],
            json={
                "data": {
                    "model_by_pk": {
                        "id": 3,
                        "sha": "adfasdfaf",
                        "model_id": "some_model_name",
                        "model_version": "some_model_variant_name",
                        "file_name": "some_model_file.onnx",
                        "updated_at": self.now.isoformat(),
                    },
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
                                "id": 4,
                            }
                        ]
                    }
                }
            },
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("ReplaceModel")],
            json={
                "data": {
                    "insert_deployment_model_configs": {
                        "id": 1,
                        "deployment_id": 2,
                        "model_config_id": 4,
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
                        "id": 2,
                        "deploy_id": "some_deployment_name",
                        "deployed": True,
                        "deployment_model_configs": [
                            {
                                "model_config": {
                                    "id": 4,
                                },
                            },
                        ],
                    },
                },
            },
        )
        add_insert_model_config_response(self.test_client.api_endpoint)
        mv = ModelVersion(client=self.test_client, data={"id": 3})
        d = Deployment(client=self.test_client, data={"id": 2})

        d = d.replace_model(mv)

        self.assertEqual(2, d.id())
        self.assertEqual(4, d.model_configs()[0].id())

    @responses.activate
    def test_status_model(self):
        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some_deployment_name",
                "deployed": False,
                "deployment_model_configs": [
                    {
                        "model_config": {
                            "id": 2,
                            "model": {
                                "id": 3,
                                "model_id": "foo-model",
                                "model_version": "v1",
                            },
                        },
                    },
                ],
                "deployment_pipeline_versions": [],
            },
        )
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("QueryLimitStatus")],
            json={"data": {"deployment": []}},
        )

        # missing server case
        with self.assertRaises(CommunicationError):
            res = deployment.status()

        self.assert_wait_for_running(deployment, CommunicationError)

        # no such model
        responses.add(
            responses.POST,
            "http://api-lb:1234/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "some_deployment_name-1"})],
            status=404,
        )
        with self.assertRaises(EntityNotFoundError):
            res = deployment.status()
        self.assert_wait_for_running(deployment, WaitForDeployError)

        responses.replace(
            responses.POST,
            "http://api-lb:1234/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "some_deployment_name-1"})],
            status=200,
            json=status_samples.ERROR,
        )
        res = deployment.status()
        self.assertEqual(res["status"], "Error")
        self.assert_wait_for_running(deployment, WaitForDeployError)

        responses.replace(
            responses.POST,
            "http://api-lb:1234/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "some_deployment_name-1"})],
            status=200,
            json=status_samples.RUNNING,
        )
        res = deployment.status()
        self.assertEqual(res["status"], "Running")
        begtime = time.time()
        dep = deployment.wait_for_running()
        endtime = time.time()
        elapsed = endtime - begtime
        self.assertTrue(elapsed <= 1)
        self.assertIsNotNone(dep)
        self.assertIsInstance(dep, Deployment)

    @responses.activate
    def test_status_pipeline(self):
        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some_deployment_name",
                "deployed": False,
                "deployment_model_configs": [
                    {
                        "model_config": {
                            "id": 2,
                        },
                    },
                ],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 3,
                        }
                    }
                ],
            },
        )

        # missing server case
        with self.assertRaises(CommunicationError):
            res = deployment.status()

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("QueryLimitStatus")],
            json={"data": {"deployment": []}},
        )

        self.assert_wait_for_running(deployment, CommunicationError)

        # no such model
        responses.add(
            responses.POST,
            "http://api-lb:1234/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "some_deployment_name-1"})],
            status=404,
        )
        with self.assertRaises(EntityNotFoundError):
            res = deployment.status()
        self.assert_wait_for_running(deployment, WaitForDeployError)

        responses.replace(
            responses.POST,
            "http://api-lb:1234/v1/api/status/get_deployment",
            status=200,
            json=status_samples.ERROR,
        )
        res = deployment.status()
        self.assertEqual(res["status"], "Error")
        self.assert_wait_for_running(deployment, WaitForDeployError)

        responses.replace(
            responses.POST,
            "http://api-lb:1234/v1/api/status/get_deployment",
            match=[responses.matchers.json_params_matcher({"name": "some_deployment_name-1"})],
            status=200,
            json=status_samples.RUNNING,
        )
        res = deployment.status()
        self.assertEqual(res["status"], "Running")

        begtime = time.time()
        dep = deployment.wait_for_running()
        endtime = time.time()
        elapsed = endtime - begtime
        self.assertTrue(elapsed <= 1)
        self.assertIsNotNone(dep)
        self.assertIsInstance(dep, Deployment)

    def test_url(self):
        deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some_deployment_name",
                "deployed": False,
                "deployment_model_configs": [
                    {
                        "model_config": {
                            "id": 2,
                        },
                    },
                ],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 3,
                        }
                    }
                ],
                "pipeline": {
                    "pipeline_id": "some_deployment_name",
                },
            },
        )
        assert (
                deployment.url()
                == "http://engine-lb.some_deployment_name-1:29502/pipelines/some_deployment_name"
        )

    def test_external_url(self):
        deployment = Deployment(
            client=self.remote_test_client,
            data={
                "id": 1,
                "deploy_id": "some_deployment_name",
                "deployed": False,
                "deployment_model_configs": [
                    {
                        "model_config": {
                            "id": 2,
                        },
                    },
                ],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 3,
                        }
                    }
                ],
                "pipeline": {
                    "pipeline_id": "some_pipeline_name",
                },
            },
        )
        print(deployment.url())
        assert (
                deployment.url()
                == "http://foo.api.org:1234/v1/api/pipelines/infer/some_deployment_name-1/some_pipeline_name"
        )


class TestDeploymentAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")
        self.test_client = wallaroo.Client(
            api_endpoint="http://api-lb:1234",
            gql_client=self.gql_client,
            auth_type="test_auth",
            request_timeout=2,  # this field used only by deployment.wait_for_running() tests
        )
        self.deployment = Deployment(
            client=self.test_client,
            data={
                "id": 1,
                "deploy_id": "some-pipeline",
                "deployed": False,
                "deployment_model_configs": [],
                "deployment_pipeline_versions": [
                    {
                        "pipeline_version": {
                            "id": 2,
                            "version": "v1",
                            "pipeline": {
                                "id": 3,
                                "pipeline_id": "some-pipeline",
                            },
                        }
                    },
                ],
                "pipeline": {
                    "pipeline_id": "some-pipeline",
                },
            },
        )

    @respx.mock
    async def test_async_infer(self):
        async with httpx.AsyncClient() as client:
            respx.post(
                "http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            ).mock(return_value=httpx.Response(200, json=SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE))
            output_df = await self.deployment.async_infer(tensor=SAMPLE_PANDAS_RECORDS_JSON, async_client=client)
            self.assertIsInstance(output_df, pd.DataFrame)
            self.assertEqual(type(output_df["time"][0]), pd.Timestamp)
            self.assertEqual(type(output_df["check_failures"][0]), numpy.int64)

