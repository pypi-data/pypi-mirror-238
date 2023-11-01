from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.model_status import ModelStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.conversion import Conversion
  from ..models.file_info import FileInfo





T = TypeVar("T", bound="ModelVersion")


@attr.s(auto_attribs=True)
class ModelVersion:
    """ 
        Attributes:
            file_info (FileInfo):
            name (str):
            status (ModelStatus):
            visibility (str):
            workspace_id (int):
            conversion (Union[Unset, None, Conversion]):
            id (Union[Unset, int]):
            image_path (Union[Unset, None, str]):
            task_id (Union[Unset, None, str]):
     """

    file_info: 'FileInfo'
    name: str
    status: ModelStatus
    visibility: str
    workspace_id: int
    conversion: Union[Unset, None, 'Conversion'] = UNSET
    id: Union[Unset, int] = UNSET
    image_path: Union[Unset, None, str] = UNSET
    task_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file_info = self.file_info.to_dict()

        name = self.name
        status = self.status.value

        visibility = self.visibility
        workspace_id = self.workspace_id
        conversion: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.conversion, Unset):
            conversion = self.conversion.to_dict() if self.conversion else None

        id = self.id
        image_path = self.image_path
        task_id = self.task_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_info": file_info,
            "name": name,
            "status": status,
            "visibility": visibility,
            "workspace_id": workspace_id,
        })
        if conversion is not UNSET:
            field_dict["conversion"] = conversion
        if id is not UNSET:
            field_dict["id"] = id
        if image_path is not UNSET:
            field_dict["image_path"] = image_path
        if task_id is not UNSET:
            field_dict["task_id"] = task_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversion import Conversion
        from ..models.file_info import FileInfo
        d = src_dict.copy()
        file_info = FileInfo.from_dict(d.pop("file_info"))




        name = d.pop("name")

        status = ModelStatus(d.pop("status"))




        visibility = d.pop("visibility")

        workspace_id = d.pop("workspace_id")

        _conversion = d.pop("conversion", UNSET)
        conversion: Union[Unset, None, Conversion]
        if _conversion is None:
            conversion = None
        elif isinstance(_conversion,  Unset):
            conversion = UNSET
        else:
            conversion = Conversion.from_dict(_conversion)




        id = d.pop("id", UNSET)

        image_path = d.pop("image_path", UNSET)

        task_id = d.pop("task_id", UNSET)

        model_version = cls(
            file_info=file_info,
            name=name,
            status=status,
            visibility=visibility,
            workspace_id=workspace_id,
            conversion=conversion,
            id=id,
            image_path=image_path,
            task_id=task_id,
        )

        model_version.additional_properties = d
        return model_version

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
