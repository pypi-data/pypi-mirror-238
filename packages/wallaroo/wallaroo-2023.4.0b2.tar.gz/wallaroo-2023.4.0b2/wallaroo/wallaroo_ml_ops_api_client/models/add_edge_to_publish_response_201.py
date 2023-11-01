import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.pipeline_publish_status import PipelinePublishStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.add_edge_to_publish_response_201_docker_run_variables import \
      AddEdgeToPublishResponse201DockerRunVariables
  from ..models.engine_config import EngineConfig
  from ..models.pipeline_publish_helm import PipelinePublishHelm





T = TypeVar("T", bound="AddEdgeToPublishResponse201")


@attr.s(auto_attribs=True)
class AddEdgeToPublishResponse201:
    """ 
        Attributes:
            created_at (datetime.datetime):
            docker_run_variables (AddEdgeToPublishResponse201DockerRunVariables):
            engine_config (EngineConfig):
            id (int):
            pipeline_version_id (int):
            status (PipelinePublishStatus):
            updated_at (datetime.datetime):
            user_images (List[str]):
            created_by (Union[Unset, None, str]):
            engine_url (Union[Unset, None, str]):
            error (Union[Unset, None, str]): If [PipelinePublish::status] is in the [PipelinePublishStatus::Error] state,
                this should be populated with the error that occured.
            helm (Union[Unset, None, PipelinePublishHelm]):
            pipeline_url (Union[Unset, None, str]):
            pipeline_version_name (Union[Unset, None, str]):
     """

    created_at: datetime.datetime
    docker_run_variables: 'AddEdgeToPublishResponse201DockerRunVariables'
    engine_config: 'EngineConfig'
    id: int
    pipeline_version_id: int
    status: PipelinePublishStatus
    updated_at: datetime.datetime
    user_images: List[str]
    created_by: Union[Unset, None, str] = UNSET
    engine_url: Union[Unset, None, str] = UNSET
    error: Union[Unset, None, str] = UNSET
    helm: Union[Unset, None, 'PipelinePublishHelm'] = UNSET
    pipeline_url: Union[Unset, None, str] = UNSET
    pipeline_version_name: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        docker_run_variables = self.docker_run_variables.to_dict()

        engine_config = self.engine_config.to_dict()

        id = self.id
        pipeline_version_id = self.pipeline_version_id
        status = self.status.value

        updated_at = self.updated_at.isoformat()

        user_images = self.user_images




        created_by = self.created_by
        engine_url = self.engine_url
        error = self.error
        helm: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.helm, Unset):
            helm = self.helm.to_dict() if self.helm else None

        pipeline_url = self.pipeline_url
        pipeline_version_name = self.pipeline_version_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "docker_run_variables": docker_run_variables,
            "engine_config": engine_config,
            "id": id,
            "pipeline_version_id": pipeline_version_id,
            "status": status,
            "updated_at": updated_at,
            "user_images": user_images,
        })
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if engine_url is not UNSET:
            field_dict["engine_url"] = engine_url
        if error is not UNSET:
            field_dict["error"] = error
        if helm is not UNSET:
            field_dict["helm"] = helm
        if pipeline_url is not UNSET:
            field_dict["pipeline_url"] = pipeline_url
        if pipeline_version_name is not UNSET:
            field_dict["pipeline_version_name"] = pipeline_version_name

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.add_edge_to_publish_response_201_docker_run_variables import \
            AddEdgeToPublishResponse201DockerRunVariables
        from ..models.engine_config import EngineConfig
        from ..models.pipeline_publish_helm import PipelinePublishHelm
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))




        docker_run_variables = AddEdgeToPublishResponse201DockerRunVariables.from_dict(d.pop("docker_run_variables"))




        engine_config = EngineConfig.from_dict(d.pop("engine_config"))




        id = d.pop("id")

        pipeline_version_id = d.pop("pipeline_version_id")

        status = PipelinePublishStatus(d.pop("status"))




        updated_at = isoparse(d.pop("updated_at"))




        user_images = cast(List[str], d.pop("user_images"))


        created_by = d.pop("created_by", UNSET)

        engine_url = d.pop("engine_url", UNSET)

        error = d.pop("error", UNSET)

        _helm = d.pop("helm", UNSET)
        helm: Union[Unset, None, PipelinePublishHelm]
        if _helm is None:
            helm = None
        elif isinstance(_helm,  Unset):
            helm = UNSET
        else:
            helm = PipelinePublishHelm.from_dict(_helm)




        pipeline_url = d.pop("pipeline_url", UNSET)

        pipeline_version_name = d.pop("pipeline_version_name", UNSET)

        add_edge_to_publish_response_201 = cls(
            created_at=created_at,
            docker_run_variables=docker_run_variables,
            engine_config=engine_config,
            id=id,
            pipeline_version_id=pipeline_version_id,
            status=status,
            updated_at=updated_at,
            user_images=user_images,
            created_by=created_by,
            engine_url=engine_url,
            error=error,
            helm=helm,
            pipeline_url=pipeline_url,
            pipeline_version_name=pipeline_version_name,
        )

        add_edge_to_publish_response_201.additional_properties = d
        return add_edge_to_publish_response_201

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
