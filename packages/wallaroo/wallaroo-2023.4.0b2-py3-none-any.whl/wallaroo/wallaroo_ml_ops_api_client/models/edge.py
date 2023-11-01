from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Edge")


@attr.s(auto_attribs=True)
class Edge:
    """ The Edge

        Attributes:
            cpus (float): Number of CPUs
            id (str): ID
            memory (str): Amount of memory (in k8s format)
            name (str): User-given name
            tags (List[str]): Edge tags
            pipeline_version_id (Union[Unset, None, int]): Pipeline version ID that is supposed to be deployed on this edge
            spiffe_id (Union[Unset, None, str]): Spiffe ID
     """

    cpus: float
    id: str
    memory: str
    name: str
    tags: List[str]
    pipeline_version_id: Union[Unset, None, int] = UNSET
    spiffe_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        cpus = self.cpus
        id = self.id
        memory = self.memory
        name = self.name
        tags = self.tags




        pipeline_version_id = self.pipeline_version_id
        spiffe_id = self.spiffe_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cpus": cpus,
            "id": id,
            "memory": memory,
            "name": name,
            "tags": tags,
        })
        if pipeline_version_id is not UNSET:
            field_dict["pipeline_version_id"] = pipeline_version_id
        if spiffe_id is not UNSET:
            field_dict["spiffe_id"] = spiffe_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cpus = d.pop("cpus")

        id = d.pop("id")

        memory = d.pop("memory")

        name = d.pop("name")

        tags = cast(List[str], d.pop("tags"))


        pipeline_version_id = d.pop("pipeline_version_id", UNSET)

        spiffe_id = d.pop("spiffe_id", UNSET)

        edge = cls(
            cpus=cpus,
            id=id,
            memory=memory,
            name=name,
            tags=tags,
            pipeline_version_id=pipeline_version_id,
            spiffe_id=spiffe_id,
        )

        edge.additional_properties = d
        return edge

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
