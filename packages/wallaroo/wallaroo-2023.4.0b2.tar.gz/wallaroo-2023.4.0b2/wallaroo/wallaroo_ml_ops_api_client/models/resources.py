from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.resources_spec import ResourcesSpec





T = TypeVar("T", bound="Resources")


@attr.s(auto_attribs=True)
class Resources:
    """ 
        Attributes:
            resources (Union[Unset, None, ResourcesSpec]):
     """

    resources: Union[Unset, None, 'ResourcesSpec'] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        resources: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources.to_dict() if self.resources else None


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if resources is not UNSET:
            field_dict["resources"] = resources

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.resources_spec import ResourcesSpec
        d = src_dict.copy()
        _resources = d.pop("resources", UNSET)
        resources: Union[Unset, None, ResourcesSpec]
        if _resources is None:
            resources = None
        elif isinstance(_resources,  Unset):
            resources = UNSET
        else:
            resources = ResourcesSpec.from_dict(_resources)




        resources = cls(
            resources=resources,
        )

        resources.additional_properties = d
        return resources

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
