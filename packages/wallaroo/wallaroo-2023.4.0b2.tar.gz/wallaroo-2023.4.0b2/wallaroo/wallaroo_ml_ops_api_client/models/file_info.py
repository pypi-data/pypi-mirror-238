from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="FileInfo")


@attr.s(auto_attribs=True)
class FileInfo:
    """ 
        Attributes:
            file_name (str):
            sha (str):
            version (str):
     """

    file_name: str
    sha: str
    version: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file_name = self.file_name
        sha = self.sha
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_name": file_name,
            "sha": sha,
            "version": version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_name = d.pop("file_name")

        sha = d.pop("sha")

        version = d.pop("version")

        file_info = cls(
            file_name=file_name,
            sha=sha,
            version=version,
        )

        file_info.additional_properties = d
        return file_info

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
