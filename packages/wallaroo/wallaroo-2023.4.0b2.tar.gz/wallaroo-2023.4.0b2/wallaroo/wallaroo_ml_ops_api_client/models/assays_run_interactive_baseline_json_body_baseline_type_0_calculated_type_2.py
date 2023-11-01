from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
  from ..models.assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_2_sliding_window import \
      AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType2SlidingWindow





T = TypeVar("T", bound="AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType2")


@attr.s(auto_attribs=True)
class AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType2:
    """ 
        Attributes:
            sliding_window (AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType2SlidingWindow):
     """

    sliding_window: 'AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType2SlidingWindow'
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        sliding_window = self.sliding_window.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "sliding_window": sliding_window,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_2_sliding_window import \
            AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType2SlidingWindow
        d = src_dict.copy()
        sliding_window = AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType2SlidingWindow.from_dict(d.pop("sliding_window"))




        assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_2 = cls(
            sliding_window=sliding_window,
        )

        assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_2.additional_properties = d
        return assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_2

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
