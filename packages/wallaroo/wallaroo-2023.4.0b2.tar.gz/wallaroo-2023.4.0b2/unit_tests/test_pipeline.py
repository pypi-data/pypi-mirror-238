import datetime
import json
import os
import unittest
from unittest import mock

import httpx
import numpy
import pandas as pd
import pyarrow as pa
import responses
import respx

import wallaroo
from wallaroo.model_version import ModelVersion
from wallaroo.model_config import ModelConfig
from wallaroo.pipeline import Pipeline
from wallaroo.pipeline_version import PipelineVersion
from wallaroo.tag import Tag
from .reusable_responders import (
    add_deployment_for_pipeline_responder,
    add_deployment_by_id_responder
)

from . import testutil

with open("unit_tests/outputs/sample_inference_result.json", "r") as fp:
    SAMPLE_INFERENCE_RESULT = json.loads(fp.read())

with open("unit_tests/outputs/sample_batched_inference_result.json", "r") as fp:
    SAMPLE_BATCHED_INFERENCE_RESULT = json.loads(fp.read())

sink = pa.BufferOutputStream()
with pa.ipc.open_file("unit_tests/outputs/sample_logs.arrow") as reader:
    arrow_logs = reader.read_all()
    with pa.ipc.new_file(sink, arrow_logs.schema) as arrow_ipc:
        arrow_ipc.write(arrow_logs)
        arrow_ipc.close()

dropped_log_sink = pa.BufferOutputStream()
with pa.ipc.open_file("unit_tests/outputs/tensor_dropped_log_file.arrow") as tdl_reader:
    tensor_dropped_logs = tdl_reader.read_all()
    with pa.ipc.new_file(dropped_log_sink, tensor_dropped_logs.schema) as tdl_ipc:
        tdl_ipc.write(tensor_dropped_logs)
        tdl_ipc.close()

SAMPLE_ARROW_LOGS_RESPONSE = sink.getvalue()
SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE = json.load(
    open('unit_tests/outputs/sample_inference_result.pandas.json', 'rb'))
with open("unit_tests/outputs/dev_smoke_test.pandas.json", "r") as fp:
    SAMPLE_PANDAS_RECORDS_JSON = pd.read_json(fp)


def logged_inference():
    with open("unit_tests/outputs/sample_logged_inference_result.json", "r") as fp:
        return json.loads(fp.read())


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.ix = 0
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(
            endpoint="http://api-lb:8080/v1/graphql"
        )
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client, auth_type="test_auth"
        )
        self.pipeline = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "x",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

    def gen_id(self):
        self.ix += 1
        return self.ix

    def ccfraud_model(self, variant="some_model_variant_name"):
        data = {
            "id": self.gen_id(),
            "model_id": "some_model_name",
            "model_version": variant,
            "sha": "ccfraud_sha",
            "file_name": "some_model_file.onnx",
            "updated_at": self.now.isoformat(),
            "visibility": "private",
        }

        model = ModelVersion(
            client=self.test_client,
            data=data,
        )
        model._config = ModelConfig(
            client=self.test_client,
            data={
                "id": self.gen_id(),
                "model": {
                    "id": model.id(),
                },
                "runtime": "onnx",
                "tensor_fields": "foo bar baz",
            },
        )
        model._config._model_version = model
        return model

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

    @staticmethod
    def add_get_topic_name_responder():
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/api/plateau/get_topic_name",
            match=[responses.matchers.json_params_matcher({"pipeline_pk_id": 1})],
            status=200,
            json={"topic_name": "workspace-1-pipeline-x-inference"},
        )

    @staticmethod
    def add_get_records_responder(params):
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference/records",
            status=200,
            body=sink.getvalue(),
            match=[responses.matchers.query_param_matcher(
                params
            )
            ],
        )

    @staticmethod
    def add_get_tensor_dropped_records_responder(params):
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference/records",
            status=200,
            body=dropped_log_sink.getvalue(),
            match=[responses.matchers.query_param_matcher(
                params
            )
            ],
        )

    @staticmethod
    def add_user_workspace_responder():
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
                                "archived": False,
                                "created_at": "2022-02-15T09:42:12.857637+00:00",
                                "created_by": "bb2dec32-09a1-40fd-8b34-18bd61c9c070",
                                "name": f"Unused",
                                "id": 1,
                                "pipelines": [],
                                "models": [],
                            }
                        }
                    ]
                }
            },
        )

    @responses.activate
    def test_init_full_dict(self):

        pipeline = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "test-pipeline",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

        self.assertEqual(1, pipeline.id())
        self.assertEqual("test-pipeline", pipeline.name())
        self.assertEqual(self.now, pipeline.create_time())
        self.assertEqual(self.now, pipeline.last_update_time())
        self.assertIsInstance(pipeline.versions()[0], PipelineVersion)

    @responses.activate
    def test_html_repr(self):

        self.add_pipeline_by_id_responder()
        add_deployment_for_pipeline_responder()
        self.add_pipeline_models_responder()
        self.add_pipeline_variant_by_id_responder()

        model1 = self.ccfraud_model("one")
        model2 = self.ccfraud_model("two")
        p = self.pipeline.add_model_step(model1)
        p = p.add_model_step(model2)

        hstr = p._repr_html_()
        self.assertTrue("<table>" in hstr)

    @responses.activate
    def test_rehydrate(self):

        testcases = [
            ("name", "test-pipeline"),
            ("create_time", self.now),
            ("last_update_time", self.now),
            ("versions", None),
        ]
        for method_name, want_value in testcases:
            with self.subTest():
                responses.add(
                    responses.POST,
                    "http://api-lb:8080/v1/graphql",
                    status=200,
                    match=[testutil.query_name_matcher("PipelineById")],
                    json={
                        "data": {
                            "pipeline_by_pk": {
                                "id": 1,
                                "pipeline_id": "test-pipeline",
                                "created_at": self.now.isoformat(),
                                "updated_at": self.now.isoformat(),
                                "pipeline_versions": [{"id": 1}],
                                "visibility": "pUbLIC",
                            }
                        },
                    },
                )

                pipeline = Pipeline(client=self.test_client, data={"id": 1})
                got_value = getattr(pipeline, method_name)()

                if want_value is not None:
                    self.assertEqual(want_value, got_value)
                self.assertEqual(1, len(responses.calls))
                # Another call to the same accessor shouldn't trigger any
                # additional GraphQL queries.
                got_value = getattr(pipeline, method_name)()
                if want_value is not None:
                    self.assertEqual(want_value, got_value)
                self.assertEqual(1, len(responses.calls))
                responses.reset()

    @responses.activate
    @mock.patch.dict(os.environ, {"ARROW_ENABLED": "false"})
    def test_logs(self):
        self.add_get_topic_name_responder()
        self.add_user_workspace_responder()

        responses.add(
            responses.GET,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference",
            status=200,
            json={
                "partitions": {
                    "testing-1": {"start": 0, "end": 20},
                    "testing-2": {"start": 0, "end": 20},
                }
            },
        )

        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/workspace-1-pipeline-x-inference/records",
            status=200,
            json={
                "records": [
                    '{"model_name":"x","model_version":"0002","pipeline_id":"","outputs":[{"Float":{"v":1,"dim":[1,1],"data":[-0.000041961669921875]}}],"elapsed":43059,"time":1642193935934,"original_data":{"tensor":[[0.0]]},"check_failures":[]}'
                ],
                "status": "All",
            },
            match=[responses.matchers.json_params_matcher({"testing-1": 10, "testing-2": 10})],
        )

        self.assertEqual(len(self.pipeline.logs(20)), 1)

    @responses.activate
    def test_logs_with_arrow(self):
        params = {
                    "page_size": 100,
                    "order": "desc",
                    "dataset[]": "*",
                    "dataset.separator": ".",
                }
        self.add_get_topic_name_responder()
        self.add_user_workspace_responder()
        self.add_get_records_responder(params)
        log_table = self.pipeline.logs(limit=100, arrow=True)
        
        self.assertIsInstance(log_table, pa.Table)
        log_table.equals(arrow_logs)

    @responses.activate
    def test_tensor_dropped_logs_with_arrow(self):
        params = {
            "page_size": 100,
            "order": "desc",
            "dataset[]": "*",
            "dataset.separator": ".",
        }
        self.add_get_topic_name_responder()
        self.add_user_workspace_responder()
        self.add_get_tensor_dropped_records_responder(params)
        log_table_df = self.pipeline.logs(limit=100)
        self.assertIsInstance(log_table_df, pd.DataFrame)
        self.assertIsNone(log_table_df["in.tensor"][0]) # tensor dropped

    @responses.activate
    def test_export_logs_to_arrow_file(self):
        start_datetime = datetime.datetime.utcnow()
        end_datetime = datetime.datetime.utcnow()
        params = {
            "time.start": start_datetime.astimezone(tz=datetime.timezone.utc).isoformat(),
            "time.end": end_datetime.astimezone(tz=datetime.timezone.utc).isoformat(),
            "dataset[]": "*",
            "dataset[]": "*",
            "dataset.separator": ".",
        }
        self.add_get_topic_name_responder()
        self.add_get_records_responder(params)

        self.pipeline.export_logs(directory="unit_tests/outputs", file_prefix="test_logs", start_datetime=start_datetime,
                                  end_datetime=end_datetime, arrow=True)
        with pa.ipc.open_file("unit_tests/outputs/test_logs-1.arrow") as file_reader:
            entries = file_reader.read_all()
        arrow_logs.equals(entries, check_metadata=True)

    @responses.activate
    def test_export_logs_without_user_provided_filepath(self):
        start_datetime = datetime.datetime.utcnow()
        end_datetime = datetime.datetime.utcnow()
        params = {
            "time.start": start_datetime.astimezone(tz=datetime.timezone.utc).isoformat(),
            "time.end": end_datetime.astimezone(tz=datetime.timezone.utc).isoformat(),
            "dataset[]": "*",
            "dataset.separator": ".",
        }
        self.add_get_topic_name_responder()
        self.add_get_records_responder(params)
        cwd = os.getcwd()
        # we don't want to be writing test related files outside this directory
        os.chdir("unit_tests/outputs")
        self.pipeline.export_logs(start_datetime=start_datetime, end_datetime=end_datetime, arrow=True)
        with pa.ipc.open_file(f"logs/{self.pipeline.name()}-1.arrow") as file_reader:
            entries = file_reader.read_all()
        arrow_logs.equals(entries, check_metadata=True)
        os.chdir(cwd)

    @responses.activate
    def test_get_pipeline_logs_by_time(self):
        start_datetime = datetime.datetime.utcnow()
        end_datetime = datetime.datetime.utcnow()
        params = {
            "time.start": start_datetime.astimezone(tz=datetime.timezone.utc).isoformat(),
            "time.end": end_datetime.astimezone(tz=datetime.timezone.utc).isoformat(),
            "dataset[]": "*",
            "dataset.separator": ".",
        }
        self.add_get_topic_name_responder()
        self.add_user_workspace_responder()
        self.add_get_records_responder(params)

        log_table = self.pipeline.logs(start_datetime=start_datetime, end_datetime=end_datetime, arrow=True)
        self.assertIsInstance(log_table, pa.Table)
        log_table.equals(arrow_logs)

    @responses.activate
    @mock.patch.dict(os.environ, {"ARROW_ENABLED": "false"})
    def test_log_time_shift(self):
        workspace_id = 1
        self.add_get_topic_name_responder()
        self.add_user_workspace_responder()
        add_deployment_for_pipeline_responder(self.test_client.api_endpoint)

        add_deployment_by_id_responder(self.test_client.api_endpoint)

        topic = f"workspace-{workspace_id}-pipeline-x-inference"
        responses.add(
            responses.GET,
            f"http://api-lb:8080/v1/logs/topic/{topic}",
            status=200,
            json={
                "partitions": {
                    "testing-1": {"start": 0, "end": 20},
                    "testing-2": {"start": 0, "end": 20},
                }
            },
        )

        prior = logged_inference()
        prior["time"] = SAMPLE_INFERENCE_RESULT[0]["time"] - 1
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/{topic}/records",
            status=200,
            json={"records": [json.dumps(prior)], "status": "All"},
            match=[responses.matchers.json_params_matcher({"testing-1": 10, "testing-2": 10})],
        )
        ready = logged_inference()
        ready["time"] = SAMPLE_INFERENCE_RESULT[0]["time"]
        responses.add(
            responses.POST,
            f"http://api-lb:8080/v1/logs/topic/{topic}/records",
            status=200,
            json={"records": [json.dumps(prior), json.dumps(ready)], "status": "All"},
            match=[responses.matchers.json_params_matcher({"testing-1": 10, "testing-2": 10})],
        )

        responses.add(
            responses.POST,
            f"http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            status=200,
            json=SAMPLE_INFERENCE_RESULT,
        )

        self.pipeline.infer({})

        self.assertEqual(len(self.pipeline.logs(20)), 2)

    @responses.activate
    def test_pipeline_building(self):
        model = self.ccfraud_model()
        p = self.pipeline.add_model_step(model)
        p = p.add_validation("no_high_fraud", model.outputs[0][0] < 0.95)
        p = p.add_validation(
            "really_no_high_fraud", model.config().outputs[0][0] < 0.95
        )

        self.assertEqual(len(p.steps()), 3)

    # This can't work yet
    # def test_pipeline_clear(self):
    #     pipeline = Pipeline(
    #         client=self.test_client,
    #         data={
    #             "id": 1,
    #             "pipeline_id": "x",
    #             "created_at": self.now.isoformat(),
    #             "updated_at": self.now.isoformat(),
    #             "pipeline_versions": [{"id": 1}],
    #             "visibility": "PUBLIC",
    #         },
    #     )
    #     one = self.ccfraud_model("one")
    #     two = self.ccfraud_model("two")
    #     pipeline.add_model_step(one)
    #     pipeline.add_model_step(two)
    #     self.assertEqual(len(pipeline.steps()), 2)
    #     self.assertEqual(len(pipeline.model_configs()), 2)

    #     result = pipeline.clear()
    #     assert isinstance(result, Pipeline)
    #     self.assertEqual(pipeline.steps(), [])
    #     self.assertEqual(pipeline.model_configs(), [])

    @responses.activate
    def test_pipeline_tags(self):

        tag_1 = Tag(client=self.test_client, data={"id": 1, "tag": "bartag314"})
        tag_2 = Tag(client=self.test_client, data={"id": 2, "tag": "footag123"})

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("PipelineById")],
            json={
                "data": {
                    "pipeline_by_pk": {
                        "id": 1,
                        "pipeline_id": "test-pipeline",
                        "created_at": self.now.isoformat(),
                        "updated_at": self.now.isoformat(),
                        "pipeline_versions": [{"id": 1}],
                        "visibility": "pUbLIC",
                        "pipeline_tags": [
                            {"tag": {"id": 1, "tag": "bartag314"}},
                            {"tag": {"id": 2, "tag": "footag123"}},
                        ],
                    }
                },
            },
        )

        pipeline = Pipeline(client=self.test_client, data={"id": 1})
        self.assertListEqual(list(map(vars, [tag_1, tag_2])), list(map(vars, pipeline.tags())))


class TestPipelineAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.id = 0
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(
            endpoint="http://api-lb:8080/v1/graphql"
        )
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client, auth_type="test_auth"
        )
        self.pipeline = Pipeline(
            client=self.test_client,
            data={
                "id": 1,
                "pipeline_id": "some-pipeline",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "pipeline_versions": [{"id": 1}],
                "visibility": "pUbLIC",
            },
        )

    @respx.mock
    @responses.activate
    async def test_async_infer(self):
        async with httpx.AsyncClient() as client:
            async_infer_route = respx.post(
                "http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
            ).mock(return_value=httpx.Response(200, json=SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE))
            add_deployment_for_pipeline_responder(self.test_client.api_endpoint)
            add_deployment_by_id_responder(self.test_client.api_endpoint)
            output_df = await self.pipeline.async_infer(tensor=SAMPLE_PANDAS_RECORDS_JSON, async_client=client)
            self.assertIsInstance(output_df, pd.DataFrame)
            self.assertEqual(type(output_df["time"][0]), pd.Timestamp)
            self.assertEqual(type(output_df["check_failures"][0]), numpy.int64)
            self.assertTrue(async_infer_route.called)
            self.assertEqual(async_infer_route.call_count, 1)

    @respx.mock
    @responses.activate
    async def test_parallel_infer(self):
        dataset = []
        for i in range(3):
            dataset.append(SAMPLE_PANDAS_RECORDS_JSON)
        infer_route = respx.post(
            "http://engine-lb.some-pipeline-1:29502/pipelines/some-pipeline",
        ).mock(return_value=httpx.Response(200, json=SAMPLE_PANDAS_RECORDS_INFERENCE_RESPONSE))

        add_deployment_for_pipeline_responder(self.test_client.api_endpoint)
        add_deployment_by_id_responder(self.test_client.api_endpoint)
        output_list = await self.pipeline.parallel_infer(tensor_list=dataset, num_parallel=3)
        self.assertIsInstance(output_list, list)
        self.assertEqual(len(output_list), 3)
        self.assertTrue(infer_route.called)
        self.assertEqual(infer_route.call_count, 3)
