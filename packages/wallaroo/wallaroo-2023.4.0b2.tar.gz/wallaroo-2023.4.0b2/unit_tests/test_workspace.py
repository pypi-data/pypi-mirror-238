import wallaroo
from wallaroo.workspace import *
from wallaroo.model_version import ModelVersion
from wallaroo.pipeline import Pipeline

import responses
import datetime
import json
import os
import pytest
from . import testutil
import httpx
import respx


class TestWorkspace:
    def setup_method(self):
        self.ix = 0
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(
            endpoint="http://api-lb:8080/v1/graphql",
        )
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client,
            auth_endpoint="http://mock-keycloak:1234",
            auth_type="test_auth",
        )

    def add_user_responder(self):
        responses.add(
            responses.GET,
            "http://mock-keycloak:1234/auth/admin/realms/master/users",
            status=200,
            json=[
                {
                    "id": "99cace15-e0d4-4bb6-bf14-35efee181b90",
                    "createdTimestamp": 1645626193993,
                    "username": "ci",
                    "enabled": True,
                    "totp": False,
                    "emailVerified": True,
                    "email": "x@c.co",
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
            ],
        )

    def add_workspace_user_create_responder(self):
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/workspaces/add_user",
            status=200,
            json={},
        )

    def add_user_by_id_responder(self, n: int):
        responses.add(
            responses.GET,
            f"http://mock-keycloak:1234/auth/admin/realms/master/users/{n}",
            status=200,
            json={
                "id": "99cace15-e0d4-4bb6-bf14-35efee181b90",
                "createdTimestamp": 1645626193993,
                "username": "ci",
                "enabled": True,
                "totp": False,
                "emailVerified": True,
                "email": "x@c.co",
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
        )

    def add_create_workspace_responder(self, respx_mock, expected_id=1):
        respx_mock.post(
            f"{self.test_client.api_endpoint}/v1/api/workspaces/create"
        ).mock(return_value=httpx.Response(200, json={"workspace_id": expected_id}))

    def add_list_workspace_responder(self, respx_mock):
        list_workspace_resp = {
            "workspaces": [
                {
                    "id": 1,
                    "name": "test-workspace",
                    "created_at": "2022-03-02T08:13:38.627443",
                    "created_by": "44",
                    "pipelines": [],
                    "models": {"models": []},
                    "users": [],
                    "archived": False,
                }
            ]
        }
        respx_mock.post(f"{self.test_client.api_endpoint}/v1/api/workspaces/list").mock(
            return_value=httpx.Response(200, json=list_workspace_resp)
        )

    def teardown_module(self):
        pass

    def test_init_full_dict(self):
        ws = Workspace(
            client=self.test_client,
            data={
                "id": 1,
                "name": "myws",
                "archived": False,
                "models": [{"id": 1}, {"id": 2}],
                "pipelines": [{"id": 1}],
                "created_at": self.now.isoformat(),
                "created_by": 42,
                "users": [{"id": 7}, {"id": 8}],
            },
        )

        assert 1 == ws.id()
        assert "myws" == ws.name()
        assert 2 == len(ws._models)
        assert 1 == len(ws._pipelines)
        assert ws._models[0]["id"] == 1
        assert ws._models[1]["id"] == 2
        assert ws._pipelines[0]["id"] == 1
        assert str(self.now.isoformat()) == ws.created_at()

    @responses.activate
    def test_rehydrate(self):
        testcases = [
            ("name", "test-workspace"),
            ("created_at", self.now.isoformat()),
            ("created_by", 44),
            ("models", []),
            ("pipelines", []),
            ("archived", False),
        ]
        for method_name, want_value in testcases:
            responses.add(
                responses.POST,
                "http://api-lb:8080/v1/graphql",
                status=200,
                match=[testutil.query_name_matcher("WorkspaceById")],
                json={
                    "data": {
                        "workspace_by_pk": {
                            "id": 1,
                            "name": "test-workspace",
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

            ws = Workspace(client=self.test_client, data={"id": 1})
            got_value = getattr(ws, method_name)()

            if want_value is not None:
                assert want_value == got_value
            if method_name == "models" or method_name == "pipelines":
                assert 2 == len(responses.calls)
            else:
                assert 1 == len(responses.calls)

            # Another call to the same accessor shouldn't trigger any
            # additional GraphQL queries.
            got_value = getattr(ws, method_name)()
            if want_value is not None:
                assert want_value == got_value

            if method_name == "models" or method_name == "pipelines":
                assert 3 == len(responses.calls)
            else:
                assert 1 == len(responses.calls)
            responses.reset()

    @responses.activate
    def test_get_user_default_workspace(self):
        client = self.test_client
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

        ws = Workspace._get_user_default_workspace(client)
        assert isinstance(ws, Workspace)
        assert ws.id() == 1
        assert ws.archived() == False
        assert ws.name() == "345fr"
        assert ws._pipelines == []
        assert ws._models == []

    @responses.activate
    def test_create_user_default_workspace(self):
        client = self.test_client
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("CreateDefaultUserWorkspace")],
            json={"data": {"insert_workspace_one": {"id": 5}}},
        )
        ws = Workspace._create_user_default_workspace(client)
        assert ws._id == 5

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_create_workspace(self, respx_mock):
        client = self.test_client

        self.add_create_workspace_responder(respx_mock, expected_id=11)

        ws = Workspace._create_workspace(client, name="foo")
        assert isinstance(ws, Workspace)
        assert ws.id() == 11

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_list_workspaces(self, respx_mock):
        self.add_list_workspace_responder(respx_mock)
        wss = self.test_client.list_workspaces()
        assert len(wss) > 0
        assert isinstance(wss[0], Workspace)
        assert wss[0].id() == 1

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_list_workspaces_html(self, respx_mock):
        self.add_list_workspace_responder(respx_mock)

        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("WorkspaceById")],
            json={
                "data": {
                    "workspace_by_pk": {
                        "id": 1,
                        "name": "test-workspace",
                        "created_at": "2022-03-02T08:13:38.627443",
                        "created_by": 44,
                        "pipelines": [],
                        "models": [],
                        "users": [],
                        "archived": False,
                    }
                },
            },
        )

        wstr = self.test_client.list_workspaces()._repr_html_()
        assert isinstance(wstr, str)
        assert "<table>" in wstr
        assert "<td>2022-03-02 08:13:38</td>" in wstr

    def test_get_set_current_workspace(self):
        client = self.test_client
        ws = Workspace(
            client=client,
            data={
                "id": 1,
            },
        )

        res1 = client.set_current_workspace(ws)
        assert isinstance(res1, Workspace)
        assert ws == res1

        res2 = client.get_current_workspace()
        assert ws == res2

    @responses.activate
    def test_users(self):
        self.add_user_by_id_responder("UUID-3")
        self.add_user_by_id_responder("UUID-4")
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("WorkspaceById")],
            json={
                "data": {
                    "workspace_by_pk": {
                        "id": 1,
                        "name": "test-workspace",
                        "created_at": self.now.isoformat(),
                        "created_by": 44,
                        "pipelines": [],
                        "models": [],
                        "users": [{"user_id": "UUID-3"}, {"user_id": "UUID-4"}],
                        "archived": False,
                    }
                },
            },
        )

        ws = Workspace(client=self.test_client, data={"id": 1})
        users = ws.users()
        assert len(users) == 2
        assert users[0].id() == "99cace15-e0d4-4bb6-bf14-35efee181b90"

    @responses.activate
    def test_add_user(self):
        self.add_user_responder()
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/workspaces/add_user",
            status=200,
        )
        ws = Workspace(
            client=self.test_client,
            data={
                "id": 1,
            },
        )

        newws = ws.add_owner("jane@ex.co")
        assert isinstance(newws, Workspace)
        assert newws._id == 1

    @responses.activate
    def test_add_owner(self):
        self.add_user_responder()
        responses.add(
            responses.POST,
            f"{self.test_client.api_endpoint}/v1/api/workspaces/add_user",
            status=200,
        )
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.mutation_name_matcher("InsertWorkspaceUser")],
            json={"data": {"insert_workspace_users_one": {"id": 2}}},
        )
        ws = Workspace(
            client=self.test_client,
            data={
                "id": 1,
            },
        )

        newws = ws.add_owner("jane@ex.co")
        assert isinstance(newws, Workspace)
        assert newws._id == 1

    @responses.activate
    @respx.mock(assert_all_mocked=True)
    def test_models(self, respx_mock):
        """
        Test that Workspaces count the appropriate number of models returned from the query.
        """
        responses.add(
            responses.POST,
            "http://api-lb:8080/v1/graphql",
            status=200,
            match=[testutil.query_name_matcher("WorkspaceById")],
            json={
                "data": {
                    "workspace_by_pk": {
                        "id": 1,
                        "name": "test-workspace",
                        "created_at": self.now.isoformat(),
                        "created_by": 44,
                        "pipelines": [],
                        "models": [{"id": 1}, {"id": 2}],
                        "users": [{"user_id": "UUID-3"}, {"user_id": "UUID-4"}],
                        "archived": False,
                    }
                },
            },
        )

        ws = Workspace(client=self.test_client, data={"id": 1})
        models = ws.models()
        assert len(models) == 2

        example_models_1 = {
            "id": 1,
            "created_at": "2022-10-26T14:12:41.040083+00:00",
            "name": "kerasccfraud",
            "owner_id": '""',
            "updated_at": "2022-10-26T14:12:41.040083+00:00",
            "models": [
                {
                    "id": 1,
                    "model_id": "kerasccfraud",
                    "model_version": "df0c6c5e-e0ee-41bc-9d6d-57ace8552b8d",
                    "models_pk_id": 1,
                    "sha": "bc85ce596945f876256f41515c7501c399fd97ebcb9ab3dd41bf03f8937b4507",
                    "file_name": "keras_ccfraud.onnx",
                    "image_path": None,
                    "updated_at": "2022-10-26T14:12:41.040083+00:00",
                    "visibility": "private",
                    "owner_id": '""',
                }
            ],
        }

        respx_mock.post(f"{self.test_client.api_endpoint}/v1/api/models/get").mock(
            return_value=httpx.Response(200, json=example_models_1)
        )

        assert models[0].id() == 1
        assert models[0].name() == example_models_1["name"]
