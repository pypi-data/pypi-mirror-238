import os, json, unittest, responses
from datetime import datetime

from . import testutil
import wallaroo
from wallaroo.deployment_config import *
from wallaroo.model_version import ModelVersion


class TestDeploymentConfig(unittest.TestCase):
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

    def test_simple(self):
        config = DeploymentConfigBuilder().build()

        self.assertEqual(
            config,
            {
                "engine": {},
                "enginelb": {},
                "engineAux": {"images": {}},
                "node_selector": {},                
            },
        )

    def test_override_image(self):
        config = DeploymentConfigBuilder().image("foo_image").build()

        self.assertEqual(
            config,
            {
                "engine": {"image": "foo_image"},
                "enginelb": {},
                "engineAux": {"images": {}},
                "node_selector": {},

                
            },
        )

    def test_override_replicas(self):
        config = DeploymentConfigBuilder().replica_count(2).build()

        self.assertEqual(
            config,
            {
                "engine": {"replicas": 2},
                "enginelb": {},
                "engineAux": {"images": {}},
                "node_selector": {},
            },
        )

    def test_override_engine_params(self):
        config = DeploymentConfigBuilder().cpus(3).memory("2Gi").build()

        self.assertEqual(
            config,
            {
                "engine": {
                    "cpu": 3,
                    "resources": {
                        "limits": {"cpu": 3, "memory": "2Gi"},
                        "requests": {"cpu": 3, "memory": "2Gi"},
                    },
                },
                "enginelb": {},
                "engineAux": {"images": {}},
                "node_selector": {},

            },
        )

    def test_override_lb_params(self):
        config = DeploymentConfigBuilder().lb_cpus(3).lb_memory("2Gi").build()

        self.assertEqual(
            config,
            {
                "engine": {},
                "enginelb": {
                    "resources": {
                        "limits": {
                            "cpu": 3,
                            "memory": "2Gi",
                        },
                        "requests": {
                            "cpu": 3,
                            "memory": "2Gi",
                        },
                    }
                },
                "engineAux": {"images": {}},
                "node_selector": {},                
            },
        )

    def test_set_replica_autoscale_min_max(self):
        serial = json.dumps(
            {
                "image": "fake",
                "replicas": 1,
                "cpus": 0.1,
                "memory": "10MiB",
                "lb_cpus": 0.2,
                "lb_memory": "20MiB",
            }
        )
        os.environ["DEPLOYMENT_CONFIG"] = serial
        dc = DeploymentConfigBuilder()
        dc.replica_autoscale_min_max(minimum=1, maximum=2)
        dc = dc.build()
        self.assertEqual(1, dc["engine"]["autoscale"]["replica_min"])
        self.assertEqual(2, dc["engine"]["autoscale"]["replica_max"])
        self.assertEqual("cpu", dc["engine"]["autoscale"]["type"])
        self.assertEqual(1, dc["engine"]["replicas"])
        del os.environ["DEPLOYMENT_CONFIG"]

    def test_set_autoscale_cpu_utilization(self):
        serial = json.dumps(
            {
                "image": "fake",
                "replicas": 5,
                "cpus": 0.1,
                "memory": "10MiB",
                "lb_cpus": 0.2,
                "lb_memory": "20MiB",
            }
        )
        os.environ["DEPLOYMENT_CONFIG"] = serial
        dc = DeploymentConfigBuilder()
        dc.autoscale_cpu_utilization(20)
        dc = dc.build()
        self.assertEqual(20, dc["engine"]["autoscale"]["cpu_utilization"])
        del os.environ["DEPLOYMENT_CONFIG"]

    def test_set_replica_autoscale_min_max_min_gt_max(self):
        serial = json.dumps(
            {
                "image": "fake",
                "replicas": 5,
                "cpus": 0.1,
                "memory": "10MiB",
                "lb_cpus": 0.2,
                "lb_memory": "20MiB",
            }
        )
        os.environ["DEPLOYMENT_CONFIG"] = serial
        dc = DeploymentConfigBuilder()
        try:
            dc.replica_autoscale_min_max(minimum=2, maximum=1)
            assert False
        except RuntimeError as e:
            assert True
        finally:
            del os.environ["DEPLOYMENT_CONFIG"]

    def test_replica_count_gt_replica_max(self):
        serial = json.dumps(
            {
                "image": "fake",
                "autoscale": {"replica_max": 5},
                "cpus": 0.1,
                "memory": "10MiB",
                "lb_cpus": 0.2,
                "lb_memory": "20MiB",
            }
        )
        os.environ["DEPLOYMENT_CONFIG"] = serial
        dc = DeploymentConfigBuilder()
        try:
            dc.replica_count(7)
            assert False
        except RuntimeError as e:
            assert True
        finally:
            del os.environ["DEPLOYMENT_CONFIG"]

    def test_env_override(self):
        serial = json.dumps(
            {
                "image": "fitzroy-mini",
                "replicas": 5,
                "cpus": 0.1,
                "gpus": 0,
                "memory": "10MiB",
                "lb_cpus": 0.2,
                "lb_memory": "20MiB",
            }
        )
        os.environ["DEPLOYMENT_CONFIG"] = serial

        print(DeploymentConfigBuilder().build())
        self.assertEqual(
            DeploymentConfigBuilder().build(),
            {
                "engine": {
                    "image": "fitzroy-mini",
                    "replicas": 5,
                    "cpu": 0.1,
                    "resources": {
                        "limits": {"cpu": 0.1, "nvidia.com/gpu": 0, "memory": "10MiB"},
                        "requests": {"cpu": 0.1, "nvidia.com/gpu": 0, "memory": "10MiB"},
                    },
                    "gpu": 0,
                },
                "enginelb": {
                    "resources": {
                        "limits": {
                            "cpu": 0.2,
                            "memory": "20MiB",
                        },
                        "requests": {
                            "cpu": 0.2,
                            "memory": "20MiB",
                        },
                    }
                },
                "engineAux": {"images": {}}, 
                "node_selector": {},
            },
        )

        del os.environ["DEPLOYMENT_CONFIG"]

    @responses.activate
    def test_sidekick_options(self):
        barnacle_boy_data = {
            "data": {
                "model_by_pk": {
                    "id": 1,
                    "sha": "somethingsomething",
                    "model_id": "barnacle-boy",
                    "model_version": "123abc-456def",
                    "image_path": "ghcr.io/wallaroolabs/sidekick-example:1234qwer",
                    "updated_at": self.now.isoformat(),
                    "visibility": "private",
                },
            },
        }
        patrick_star_data = {
            "data": {
                "model_by_pk": {
                    "id": 1,
                    "sha": "somethingsomething",
                    "model_id": "patrick-star",
                    "model_version": "123abc-456def",
                    "image_path": "ghcr.io/wallaroolabs/sidekick-example:1234qwer",
                    "updated_at": self.now.isoformat(),
                    "visibility": "private",
                },
            },
        }
        responses.add(
            method=responses.POST,
            url="http://api-lb:8080/v1/graphql",
            status=200,
            match=[
                lambda req: (
                    "model_by_pk(id: 1)" in req.body.decode("UTF-8"),
                    "not found",
                ),
            ],
            json=barnacle_boy_data,
        )
        responses.add(
            method=responses.POST,
            url="http://api-lb:8080/v1/graphql",
            status=200,
            match=[
                lambda req: (
                    "model_by_pk(id: 2)" in req.body.decode("UTF-8"),
                    "not found",
                ),
            ],
            json=patrick_star_data,
        )

        barnacle_boy = ModelVersion(self.test_client, data={"id": 1})
        patrick_star = ModelVersion(self.test_client, data={"id": 2})

        config = (
            DeploymentConfigBuilder()
            .sidekick_cpus(barnacle_boy, 1.75)
            .sidekick_memory(barnacle_boy, "1Gi")
            .sidekick_env(
                barnacle_boy, {"GUNICORN_CMD_ARGS": "-timeout=120 --workers=4"}
            )
            .sidekick_cpus(patrick_star, 0.25)
            .sidekick_memory(patrick_star, "3Gi")
            .sidekick_env(
                patrick_star, {"GUNICORN_CMD_ARGS": "-timeout=240 --workers=1"}
            )
            .build()
        )
        self.assertEqual(len(config["engineAux"]["images"]), 2)

        self.assertEqual(
            config["engineAux"]["images"]["barnacle-boy-1"],
            {
                "resources": {
                    "limits": {
                        "cpu": 1.75,
                        "memory": "1Gi",
                    },
                    "requests": {
                        "cpu": 1.75,
                        "memory": "1Gi",
                    },
                },
                "env": [
                    {"name": "GUNICORN_CMD_ARGS", "value": "-timeout=120 --workers=4"}
                ],
            },
        )

        self.assertEqual(
            config["engineAux"]["images"]["patrick-star-1"],
            {
                "resources": {
                    "limits": {
                        "cpu": 0.25,
                        "memory": "3Gi",
                    },
                    "requests": {
                        "cpu": 0.25,
                        "memory": "3Gi",
                    },
                },
                "env": [
                    {"name": "GUNICORN_CMD_ARGS", "value": "-timeout=240 --workers=1"}
                ],
            },
        )

    def test_workspace_injection(self):
        config = DeploymentConfigBuilder(workspace_id=1).build()

        self.assertEqual(
            config,
            {
                "engine": {},
                "enginelb": {},
                "engineAux": {"images": {}},
                "workspace_id": 1,
                "node_selector": {},                
            },
        )
