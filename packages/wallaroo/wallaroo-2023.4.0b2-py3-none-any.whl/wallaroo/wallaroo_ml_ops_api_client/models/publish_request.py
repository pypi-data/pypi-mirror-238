from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.engine_config import EngineConfig





T = TypeVar("T", bound="PublishRequest")


@attr.s(auto_attribs=True)
class PublishRequest:
    """ Request to publish a pipeline.

        Attributes:
            model_config_ids (List[int]):
            pipeline_version_id (int):
            engine_config (Union[Unset, None, EngineConfig]):
     """

    model_config_ids: List[int]
    pipeline_version_id: int
    engine_config: Union[Unset, None, 'EngineConfig'] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        model_config_ids = self.model_config_ids




        pipeline_version_id = self.pipeline_version_id
        engine_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.engine_config, Unset):
            engine_config = self.engine_config.to_dict() if self.engine_config else None


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "model_config_ids": model_config_ids,
            "pipeline_version_id": pipeline_version_id,
        })
        if engine_config is not UNSET:
            field_dict["engine_config"] = engine_config

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.engine_config import EngineConfig
        d = src_dict.copy()
        model_config_ids = cast(List[int], d.pop("model_config_ids"))


        pipeline_version_id = d.pop("pipeline_version_id")

        _engine_config = d.pop("engine_config", UNSET)
        engine_config: Union[Unset, None, EngineConfig]
        if _engine_config is None:
            engine_config = None
        elif isinstance(_engine_config,  Unset):
            engine_config = UNSET
        else:
            engine_config = EngineConfig.from_dict(_engine_config)




        publish_request = cls(
            model_config_ids=model_config_ids,
            pipeline_version_id=pipeline_version_id,
            engine_config=engine_config,
        )

        publish_request.additional_properties = d
        return publish_request

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
