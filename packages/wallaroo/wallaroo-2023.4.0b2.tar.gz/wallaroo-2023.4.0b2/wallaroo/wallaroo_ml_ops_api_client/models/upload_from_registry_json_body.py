from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.conversion import Conversion





T = TypeVar("T", bound="UploadFromRegistryJsonBody")


@attr.s(auto_attribs=True)
class UploadFromRegistryJsonBody:
    """ Payload for the List Registries call.

        Attributes:
            conversion (Conversion):
            name (str): A descriptive, DNS-safe name for this model in the Wallaroo system.
            path (str): The path to the model file in the remote Model Registry.
            registry_id (str): The unique identifier of the Model Registry in the Wallaroo system.
            visibility (str):
            workspace_id (int):
            image_path (Union[Unset, None, str]):
            input_schema (Union[Unset, None, str]):
            output_schema (Union[Unset, None, str]):
     """

    conversion: 'Conversion'
    name: str
    path: str
    registry_id: str
    visibility: str
    workspace_id: int
    image_path: Union[Unset, None, str] = UNSET
    input_schema: Union[Unset, None, str] = UNSET
    output_schema: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        conversion = self.conversion.to_dict()

        name = self.name
        path = self.path
        registry_id = self.registry_id
        visibility = self.visibility
        workspace_id = self.workspace_id
        image_path = self.image_path
        input_schema = self.input_schema
        output_schema = self.output_schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "conversion": conversion,
            "name": name,
            "path": path,
            "registry_id": registry_id,
            "visibility": visibility,
            "workspace_id": workspace_id,
        })
        if image_path is not UNSET:
            field_dict["image_path"] = image_path
        if input_schema is not UNSET:
            field_dict["input_schema"] = input_schema
        if output_schema is not UNSET:
            field_dict["output_schema"] = output_schema

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conversion import Conversion
        d = src_dict.copy()
        conversion = Conversion.from_dict(d.pop("conversion"))




        name = d.pop("name")

        path = d.pop("path")

        registry_id = d.pop("registry_id")

        visibility = d.pop("visibility")

        workspace_id = d.pop("workspace_id")

        image_path = d.pop("image_path", UNSET)

        input_schema = d.pop("input_schema", UNSET)

        output_schema = d.pop("output_schema", UNSET)

        upload_from_registry_json_body = cls(
            conversion=conversion,
            name=name,
            path=path,
            registry_id=registry_id,
            visibility=visibility,
            workspace_id=workspace_id,
            image_path=image_path,
            input_schema=input_schema,
            output_schema=output_schema,
        )

        upload_from_registry_json_body.additional_properties = d
        return upload_from_registry_json_body

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
