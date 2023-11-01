import time
from http import HTTPStatus
from typing import TYPE_CHECKING, List, Optional, cast
from .unwrap import unwrap
import datetime
from .wallaroo_ml_ops_api_client.models.publish_pipeline_response_202 import (
    PublishPipelineResponse202,
)
from .wallaroo_ml_ops_api_client.api.pipelines.add_edge_to_publish import (
    AddEdgeToPublishJsonBody,
    sync_detailed as sync,
)
from dateutil import parser as dateparse

if TYPE_CHECKING:
    # Imports that happen below in methods to fix circular import dependency
    # issues need to also be specified here to satisfy mypy type checking.
    from .client import Client


class PipelinePublish(PublishPipelineResponse202):
    # Chart URL isn't currently returned by all routes.
    def __init__(self, client: "Client", chart_url=None, **data):
        data.setdefault("docker_run_variables", {})
        super().__init__(**data)
        self.client = client
        self.created_at = dateparse.isoparse(cast(str, data.get("created_at")))
        self.updated_at = dateparse.isoparse(cast(str, data.get("updated_at")))
        if isinstance(self.created_by, str):
            self.created_by_email = client.get_email_by_id(self.created_by)

    def _wait_for_status(self):
        from .wallaroo_ml_ops_api_client.api.pipelines.get_publish_status import (
            sync_detailed,
            GetPublishStatusJsonBody,
        )

        TIMEOUT_LIMIT = 600  # 600 seconds, or 10 minutes.

        poll_interval = 5
        expire_time = datetime.datetime.now() + datetime.timedelta(
            seconds=TIMEOUT_LIMIT
        )
        print(f"Waiting for pipeline publish... It may take up to {TIMEOUT_LIMIT} sec.")
        print(f"Pipeline is ", end="", flush=True)
        last_status = None
        while datetime.datetime.now() < expire_time:
            ret = sync_detailed(
                client=self.client.mlops(), json_body=GetPublishStatusJsonBody(self.id)
            )
            if ret.parsed is None:
                print("ERROR!")
                raise Exception(
                    f"An error occured during pipeline publish. Status API returned",
                    ret.content,
                )
            status = ret.parsed.status
            if status.lower() == "published":
                print("Published.")
                return PipelinePublish(
                    client=self.client, **unwrap(ret.parsed).to_dict()
                )
            elif status.lower() == "error":
                print(f"ERROR! {ret.parsed.error}")
                raise Exception(
                    f"An error occured during pipeline publish. {ret.parsed.error}"
                )
            else:
                if last_status != status:
                    print(
                        f"{status.replace('_', ' ').capitalize()}", end="", flush=True
                    )
                print(".", end="", flush=True)
                last_status = status
                time.sleep(poll_interval)
        else:
            raise Exception(f"Pipeline Publish timed out after {TIMEOUT_LIMIT} sec.")

    def _repr_html_(self):
        from wallaroo.wallaroo_ml_ops_api_client.types import Unset

        chart = (
            None if self.helm is None or self.helm is Unset else self.helm.get("chart")
        )
        reference = (
            None
            if self.helm is None or self.helm is Unset
            else self.helm.get("reference")
        )
        version = (
            None
            if self.helm is None or self.helm is Unset
            else self.helm.get("version")
        )

        def null_safe_a_tag(var):
            return f"<a href='https://{var}'>{var}</a>" if var is not None else None

        return f"""
          <table>
              <tr><td>ID</td><td>{self.id}</td></tr>
              <tr><td>Pipeline Version</td><td>{self.pipeline_version_name}</td></tr>
              <tr><td>Status</td><td>{self.status}</td></tr>
              <tr><td>Engine URL</td><td>{null_safe_a_tag(self.engine_url)}</td></tr>
              <tr><td>Pipeline URL</td><td>{null_safe_a_tag(self.pipeline_url)}</td></tr>
              <tr><td>Helm Chart URL</td><td>oci://{null_safe_a_tag(chart)}</td></tr>
              <tr><td>Helm Chart Reference</td><td>{reference}</td></tr>
              <tr><td>Helm Chart Version</td><td>{version}</td></tr>
              <tr><td>Engine Config</td><td>{self.engine_config}</td></tr>
              <tr><td>User Images</td><td>{self.user_images}</td></tr>
              <tr><td>Created By</td><td>{self.created_by_email}</td></tr>
              <tr><td>Created At</td><td>{self.created_at}</td></tr>
              <tr><td>Updated At</td><td>{self.updated_at}</td></tr>
              <tr><td>Docker Run Variables</td><td>{self.docker_run_variables}</td></tr>
          </table>
        """

    def add_edge(
        self,
        name: str,
        tags: List[str] = [],
    ) -> "PipelinePublish":
        """Add new edge to a published pipeline."""

        assert self.client is not None

        res = sync(
            client=self.client.mlops(),
            json_body=AddEdgeToPublishJsonBody(
                name=name,
                pipeline_publish_id=self.id,
                tags=tags,
            ),
        )
        if res.status_code != HTTPStatus.CREATED or res.parsed is None:
            raise Exception("Failed to add edge to published pipeline.", res.content)
        return PipelinePublish(client=self.client, **res.parsed.to_dict())

    def remove_edge(
        self,
        name: str,
    ):
        """Remove an edge to a published pipeline.

        :param str name: The name of the edge that will be removed. This is not limited to this pipeline.
        """
        self.client.remove_edge(name)


class PipelinePublishList(List[PipelinePublish]):
    """Wraps a list of published pipelines for display in a display-aware environment like Jupyter."""

    def _repr_html_(self) -> str:
        def row(publish: PipelinePublish):
            fmt = publish.client._time_format

            created_at = publish.created_at.strftime(fmt)
            updated_at = publish.updated_at.strftime(fmt)

            def null_safe_a_tag(var):
                return f"<a href='https://{var}'>{var}</a>" if var is not None else None

            return (
                "<tr>"
                + f"<td>{publish.id}</td>"
                + f"<td>{publish.pipeline_version_name}</td>"
                + f"<td>{null_safe_a_tag(publish.engine_url)}</td>"
                + f"<td>{null_safe_a_tag(publish.pipeline_url)}</td>"
                + f"<td>{publish.created_by_email}</td>"
                + f"<td>{created_at}</td>"
                + f"<td>{updated_at}</td>"
                + "</tr>"
            )

        fields = [
            "id",
            "pipeline_version_name",
            "engine_url",
            "pipeline_url",
            "created_by",
            "created_at",
            "updated_at",
        ]

        if self == []:
            return "(no publishes)"
        else:
            return (
                "<table>"
                + "<tr><th>"
                + "</th><th>".join(fields)
                + "</th></tr>"
                + ("".join([row(p) for p in self]))
                + "</table>"
            )
