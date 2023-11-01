from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.registered_model_version import RegisteredModelVersion





T = TypeVar("T", bound="RegisteredModel")


@attr.s(auto_attribs=True)
class RegisteredModel:
    """ A [RegisteredModel] is an MLFlow concept for a model that has been logged in MLFlow.
    For more information, see https://mlflow.org/docs/latest/model-registry.html#concepts

        Attributes:
            creation_timestamp (int): Timestamp in milliseconds from epoch
            last_updated_timestamp (int): Timestamp in milliseconds from epoch
            name (str):
            user_id (str):
            latest_versions (Union[Unset, None, List['RegisteredModelVersion']]):
     """

    creation_timestamp: int
    last_updated_timestamp: int
    name: str
    user_id: str
    latest_versions: Union[Unset, None, List['RegisteredModelVersion']] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        creation_timestamp = self.creation_timestamp
        last_updated_timestamp = self.last_updated_timestamp
        name = self.name
        user_id = self.user_id
        latest_versions: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.latest_versions, Unset):
            if self.latest_versions is None:
                latest_versions = None
            else:
                latest_versions = []
                for latest_versions_item_data in self.latest_versions:
                    latest_versions_item = latest_versions_item_data.to_dict()

                    latest_versions.append(latest_versions_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "creation_timestamp": creation_timestamp,
            "last_updated_timestamp": last_updated_timestamp,
            "name": name,
            "user_id": user_id,
        })
        if latest_versions is not UNSET:
            field_dict["latest_versions"] = latest_versions

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.registered_model_version import RegisteredModelVersion
        d = src_dict.copy()
        creation_timestamp = d.pop("creation_timestamp")

        last_updated_timestamp = d.pop("last_updated_timestamp")

        name = d.pop("name")

        user_id = d.pop("user_id")

        latest_versions = []
        _latest_versions = d.pop("latest_versions", UNSET)
        for latest_versions_item_data in (_latest_versions or []):
            latest_versions_item = RegisteredModelVersion.from_dict(latest_versions_item_data)



            latest_versions.append(latest_versions_item)


        registered_model = cls(
            creation_timestamp=creation_timestamp,
            last_updated_timestamp=last_updated_timestamp,
            name=name,
            user_id=user_id,
            latest_versions=latest_versions,
        )

        registered_model.additional_properties = d
        return registered_model

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
