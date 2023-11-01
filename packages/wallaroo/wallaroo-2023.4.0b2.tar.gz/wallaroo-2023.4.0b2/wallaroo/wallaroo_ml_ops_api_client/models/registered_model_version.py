from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisteredModelVersion")


@attr.s(auto_attribs=True)
class RegisteredModelVersion:
    """ An MLFlow version of a [RegisteredModel]. Versions start at 1.

        Attributes:
            creation_timestamp (int): Timestamp in milliseconds from epoch
            current_stage (str):
            last_updated_timestamp (int): Timestamp in milliseconds from epoch
            name (str):
            run_id (str):
            source (str):
            status (str):
            version (str):
            description (Union[Unset, None, str]):
            run_link (Union[Unset, None, str]):
            user_id (Union[Unset, None, str]):
     """

    creation_timestamp: int
    current_stage: str
    last_updated_timestamp: int
    name: str
    run_id: str
    source: str
    status: str
    version: str
    description: Union[Unset, None, str] = UNSET
    run_link: Union[Unset, None, str] = UNSET
    user_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        creation_timestamp = self.creation_timestamp
        current_stage = self.current_stage
        last_updated_timestamp = self.last_updated_timestamp
        name = self.name
        run_id = self.run_id
        source = self.source
        status = self.status
        version = self.version
        description = self.description
        run_link = self.run_link
        user_id = self.user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "creation_timestamp": creation_timestamp,
            "current_stage": current_stage,
            "last_updated_timestamp": last_updated_timestamp,
            "name": name,
            "run_id": run_id,
            "source": source,
            "status": status,
            "version": version,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if run_link is not UNSET:
            field_dict["run_link"] = run_link
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        creation_timestamp = d.pop("creation_timestamp")

        current_stage = d.pop("current_stage")

        last_updated_timestamp = d.pop("last_updated_timestamp")

        name = d.pop("name")

        run_id = d.pop("run_id")

        source = d.pop("source")

        status = d.pop("status")

        version = d.pop("version")

        description = d.pop("description", UNSET)

        run_link = d.pop("run_link", UNSET)

        user_id = d.pop("user_id", UNSET)

        registered_model_version = cls(
            creation_timestamp=creation_timestamp,
            current_stage=current_stage,
            last_updated_timestamp=last_updated_timestamp,
            name=name,
            run_id=run_id,
            source=source,
            status=status,
            version=version,
            description=description,
            run_link=run_link,
            user_id=user_id,
        )

        registered_model_version.additional_properties = d
        return registered_model_version

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
