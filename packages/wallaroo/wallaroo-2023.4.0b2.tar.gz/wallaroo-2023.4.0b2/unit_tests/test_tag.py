import json

import wallaroo
from wallaroo.tag import Tag

import datetime
import responses
import unittest

from . import testutil


class TestTag(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client, auth_type="test_auth"
        )

    @responses.activate
    def test_init_full_dict(self):

        tag = Tag(
            client=self.test_client,
            data={"id": 1, "tag": "test-tag"},
        )

        self.assertEqual(1, tag.id())
        self.assertEqual("test-tag", tag.tag())

    @responses.activate
    def test_rehydrate(self):
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("TagById")],
            json={
                "data": {
                    "tag_by_pk": {
                        "id": 999,
                        "tag": "test-tag",
                    }
                },
            },
        )

        tag = Tag(client=self.test_client, data={"id": 9999, "tag": "test-tag"})

    @responses.activate
    def test_client_create(self):
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("CreateTag")],
            json={
                "data": {"insert_tag": {"returning": [{"id": 4, "tag": "hello-tag"}]}}
            },
        )

        res = self.test_client.create_tag("hello-tag")
        self.assertIsInstance(res, Tag)
        self.assertEqual(res.tag(), "hello-tag")

    @responses.activate
    def test_add_to_model(self):
        model_id = 1111
        tag_id = 9999

        variables = {"model_id": model_id, "tag_id": tag_id}
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("AddTagToModel"), testutil.variables_matcher(json.dumps(variables))],
            json={
                "data": {
                    "insert_model_tag": {
                        "returning": [
                            variables,
                        ]
                    }
                }
            },
        )

        tag = Tag(client=self.test_client, data={"id": tag_id, "tag": "test-tag"})

        res = tag.add_to_model(model_id)

        self.assertEqual(res["tag_id"], tag_id)
        self.assertEqual(res["model_id"], model_id)

    @responses.activate
    def test_remove_from_model(self):
        model_id = 1111
        tag_id = 9999
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("RemoveTagFromModel")],
            json={
                "data": {
                    "delete_model_tag": {
                        "returning": [
                            {
                                "model_id": model_id,
                                "tag_id": tag_id,
                            },
                        ]
                    }
                }
            },
        )

        tag = Tag(client=self.test_client, data={"id": tag_id, "tag": "test-tag"})

        res = tag.remove_from_model(model_id)
        self.assertEqual(res["tag_id"], tag_id)
        self.assertEqual(res["model_id"], model_id)

    @responses.activate
    def test_add_to_pipeline(self):
        pipeline_id = 1111
        tag_id = 9999
        variables = {"pipeline_id": pipeline_id, "tag_id": tag_id}

        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("AddTagToPipeline"), testutil.variables_matcher(json.dumps(variables))],
            json={
                "data": {
                    "insert_pipeline_tag": {
                        "returning": [
                            {"tag_pk_id": tag_id, "pipeline_pk_id": pipeline_id},
                        ]
                    }
                }
            },
        )

        tag = Tag(client=self.test_client, data={"id": 9999, "tag": "test-tag"})

        res = tag.add_to_pipeline(1111)
        self.assertEqual(res["tag_pk_id"], tag_id)
        self.assertEqual(res["pipeline_pk_id"], pipeline_id)

    @responses.activate
    def test_remove_from_pipeline(self):
        pipeline_id = 1111
        tag_id = 9999
        responses.add(
            responses.POST,
            "http://api-lb/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("RemoveTagFromPipeline")],
            json={
                "data": {
                    "delete_pipeline_tag": {
                        "returning": [
                            {
                                "pipeline_pk_id": pipeline_id,
                                "tag_pk_id": tag_id,
                            },
                        ]
                    }
                }
            },
        )

        tag = Tag(client=self.test_client, data={"id": 9999, "tag": "test-tag"})

        res = tag.remove_from_pipeline(1111)
        self.assertEqual(res["tag_pk_id"], tag_id)
        self.assertEqual(res["pipeline_pk_id"], pipeline_id)
