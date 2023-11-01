import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="Pipeline")


@attr.s(auto_attribs=True)
class Pipeline:
    """ Definition of an inference pipeline that can be deployed on the edge.

        Attributes:
            created_at (datetime.datetime): When this [Pipeline] was created.
                Optional because they are read-only
            id (str): The unique identifier of a [Pipeline].
            updated_at (datetime.datetime): When this [Pipeline] was last updated.
                Optional because they are read-only
     """

    created_at: datetime.datetime
    id: str
    updated_at: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id
        updated_at = self.updated_at.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "id": id,
            "updated_at": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))




        id = d.pop("id")

        updated_at = isoparse(d.pop("updated_at"))




        pipeline = cls(
            created_at=created_at,
            id=id,
            updated_at=updated_at,
        )

        pipeline.additional_properties = d
        return pipeline

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
