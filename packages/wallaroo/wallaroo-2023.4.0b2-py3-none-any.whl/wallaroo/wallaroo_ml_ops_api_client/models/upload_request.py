from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.conversion import Conversion





T = TypeVar("T", bound="UploadRequest")


@attr.s(auto_attribs=True)
class UploadRequest:
    """ 
        Attributes:
            conversion (Conversion):
            name (str):
            visibility (str):
            workspace_id (int):
            image_path (Union[Unset, None, str]):
            input_schema (Union[Unset, None, str]):
            output_schema (Union[Unset, None, str]):
            registry_id (Union[Unset, None, str]): The unique identifier for a Registry
                Not compatible with file uploads, only used with `registry_uri` uploads
     """

    conversion: 'Conversion'
    name: str
    visibility: str
    workspace_id: int
    image_path: Union[Unset, None, str] = UNSET
    input_schema: Union[Unset, None, str] = UNSET
    output_schema: Union[Unset, None, str] = UNSET
    registry_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        conversion = self.conversion.to_dict()

        name = self.name
        visibility = self.visibility
        workspace_id = self.workspace_id
        image_path = self.image_path
        input_schema = self.input_schema
        output_schema = self.output_schema
        registry_id = self.registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "conversion": conversion,
            "name": name,
            "visibility": visibility,
            "workspace_id": workspace_id,
        })
        if image_path is not UNSET:
            field_dict["image_path"] = image_path
        if input_schema is not UNSET:
            field_dict["input_schema"] = input_schema
        if output_schema is not UNSET:
            field_dict["output_schema"] = output_schema
        if registry_id is not UNSET:
            field_dict["registry_id"] = registry_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversion import Conversion
        d = src_dict.copy()
        conversion = Conversion.from_dict(d.pop("conversion"))




        name = d.pop("name")

        visibility = d.pop("visibility")

        workspace_id = d.pop("workspace_id")

        image_path = d.pop("image_path", UNSET)

        input_schema = d.pop("input_schema", UNSET)

        output_schema = d.pop("output_schema", UNSET)

        registry_id = d.pop("registry_id", UNSET)

        upload_request = cls(
            conversion=conversion,
            name=name,
            visibility=visibility,
            workspace_id=workspace_id,
            image_path=image_path,
            input_schema=input_schema,
            output_schema=output_schema,
            registry_id=registry_id,
        )

        upload_request.additional_properties = d
        return upload_request

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
