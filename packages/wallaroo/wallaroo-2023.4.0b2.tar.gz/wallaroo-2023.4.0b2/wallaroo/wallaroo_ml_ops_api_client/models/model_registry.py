import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelRegistry")


@attr.s(auto_attribs=True)
class ModelRegistry:
    """ A reference to a remote Model Registry, such as Azure Databricks MLFlow Registry

        Attributes:
            created_at (datetime.datetime):
            name (str): A descriptive name for this registry
            token (str): A user token with access to the Registry.
                Tokens must be in base64 format.
            updated_at (datetime.datetime):
            url (str): The URL for accessing this registry
                URLs should allow MLFlow Registry API access
            id (Union[Unset, None, str]): A unique identifier for this registry
     """

    created_at: datetime.datetime
    name: str
    token: str
    updated_at: datetime.datetime
    url: str
    id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        name = self.name
        token = self.token
        updated_at = self.updated_at.isoformat()

        url = self.url
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "name": name,
            "token": token,
            "updated_at": updated_at,
            "url": url,
        })
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))




        name = d.pop("name")

        token = d.pop("token")

        updated_at = isoparse(d.pop("updated_at"))




        url = d.pop("url")

        id = d.pop("id", UNSET)

        model_registry = cls(
            created_at=created_at,
            name=name,
            token=token,
            updated_at=updated_at,
            url=url,
            id=id,
        )

        model_registry.additional_properties = d
        return model_registry

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
