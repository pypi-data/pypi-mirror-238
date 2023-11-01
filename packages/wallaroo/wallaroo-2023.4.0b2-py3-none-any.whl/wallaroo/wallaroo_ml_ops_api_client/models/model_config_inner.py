from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.runtime import Runtime
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelConfigInner")


@attr.s(auto_attribs=True)
class ModelConfigInner:
    """ Model configuration (mirrors row in model_config table in datablase)

        Attributes:
            model_version_id (int):
            runtime (Runtime): Valid runtime types
            batch_config (Union[Unset, None, str]):
            filter_threshold (Union[Unset, None, float]):
            input_schema (Union[Unset, None, str]):
            output_schema (Union[Unset, None, str]):
            tensor_fields (Union[Unset, Any]):
     """

    model_version_id: int
    runtime: Runtime
    batch_config: Union[Unset, None, str] = UNSET
    filter_threshold: Union[Unset, None, float] = UNSET
    input_schema: Union[Unset, None, str] = UNSET
    output_schema: Union[Unset, None, str] = UNSET
    tensor_fields: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        model_version_id = self.model_version_id
        runtime = self.runtime.value

        batch_config = self.batch_config
        filter_threshold = self.filter_threshold
        input_schema = self.input_schema
        output_schema = self.output_schema
        tensor_fields = self.tensor_fields

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "model_version_id": model_version_id,
            "runtime": runtime,
        })
        if batch_config is not UNSET:
            field_dict["batch_config"] = batch_config
        if filter_threshold is not UNSET:
            field_dict["filter_threshold"] = filter_threshold
        if input_schema is not UNSET:
            field_dict["input_schema"] = input_schema
        if output_schema is not UNSET:
            field_dict["output_schema"] = output_schema
        if tensor_fields is not UNSET:
            field_dict["tensor_fields"] = tensor_fields

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model_version_id = d.pop("model_version_id")

        runtime = Runtime(d.pop("runtime"))




        batch_config = d.pop("batch_config", UNSET)

        filter_threshold = d.pop("filter_threshold", UNSET)

        input_schema = d.pop("input_schema", UNSET)

        output_schema = d.pop("output_schema", UNSET)

        tensor_fields = d.pop("tensor_fields", UNSET)

        model_config_inner = cls(
            model_version_id=model_version_id,
            runtime=runtime,
            batch_config=batch_config,
            filter_threshold=filter_threshold,
            input_schema=input_schema,
            output_schema=output_schema,
            tensor_fields=tensor_fields,
        )

        model_config_inner.additional_properties = d
        return model_config_inner

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
