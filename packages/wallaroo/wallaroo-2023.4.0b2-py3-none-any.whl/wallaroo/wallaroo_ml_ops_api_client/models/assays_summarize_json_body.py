from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

if TYPE_CHECKING:
  from ..models.assays_summarize_json_body_baseline_type_0 import \
      AssaysSummarizeJsonBodyBaselineType0
  from ..models.assays_summarize_json_body_baseline_type_1 import \
      AssaysSummarizeJsonBodyBaselineType1
  from ..models.assays_summarize_json_body_baseline_type_2 import \
      AssaysSummarizeJsonBodyBaselineType2
  from ..models.assays_summarize_json_body_summarizer_type_0 import \
      AssaysSummarizeJsonBodySummarizerType0
  from ..models.assays_summarize_json_body_summarizer_type_1 import \
      AssaysSummarizeJsonBodySummarizerType1





T = TypeVar("T", bound="AssaysSummarizeJsonBody")


@attr.s(auto_attribs=True)
class AssaysSummarizeJsonBody:
    """ 
        Attributes:
            summarizer (Union['AssaysSummarizeJsonBodySummarizerType0', 'AssaysSummarizeJsonBodySummarizerType1']):
            baseline (Union['AssaysSummarizeJsonBodyBaselineType0', 'AssaysSummarizeJsonBodyBaselineType1',
                'AssaysSummarizeJsonBodyBaselineType2']):
     """

    summarizer: Union['AssaysSummarizeJsonBodySummarizerType0', 'AssaysSummarizeJsonBodySummarizerType1']
    baseline: Union['AssaysSummarizeJsonBodyBaselineType0', 'AssaysSummarizeJsonBodyBaselineType1', 'AssaysSummarizeJsonBodyBaselineType2']
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.assays_summarize_json_body_baseline_type_0 import \
            AssaysSummarizeJsonBodyBaselineType0
        from ..models.assays_summarize_json_body_baseline_type_1 import \
            AssaysSummarizeJsonBodyBaselineType1
        from ..models.assays_summarize_json_body_summarizer_type_0 import \
            AssaysSummarizeJsonBodySummarizerType0
        summarizer: Dict[str, Any]

        if isinstance(self.summarizer, AssaysSummarizeJsonBodySummarizerType0):
            summarizer = self.summarizer.to_dict()

        else:
            summarizer = self.summarizer.to_dict()



        baseline: Dict[str, Any]

        if isinstance(self.baseline, AssaysSummarizeJsonBodyBaselineType0):
            baseline = self.baseline.to_dict()

        elif isinstance(self.baseline, AssaysSummarizeJsonBodyBaselineType1):
            baseline = self.baseline.to_dict()

        else:
            baseline = self.baseline.to_dict()




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "summarizer": summarizer,
            "baseline": baseline,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assays_summarize_json_body_baseline_type_0 import \
            AssaysSummarizeJsonBodyBaselineType0
        from ..models.assays_summarize_json_body_baseline_type_1 import \
            AssaysSummarizeJsonBodyBaselineType1
        from ..models.assays_summarize_json_body_baseline_type_2 import \
            AssaysSummarizeJsonBodyBaselineType2
        from ..models.assays_summarize_json_body_summarizer_type_0 import \
            AssaysSummarizeJsonBodySummarizerType0
        from ..models.assays_summarize_json_body_summarizer_type_1 import \
            AssaysSummarizeJsonBodySummarizerType1
        d = src_dict.copy()
        def _parse_summarizer(data: object) -> Union['AssaysSummarizeJsonBodySummarizerType0', 'AssaysSummarizeJsonBodySummarizerType1']:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summarizer_type_0 = AssaysSummarizeJsonBodySummarizerType0.from_dict(data)



                return summarizer_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            summarizer_type_1 = AssaysSummarizeJsonBodySummarizerType1.from_dict(data)



            return summarizer_type_1

        summarizer = _parse_summarizer(d.pop("summarizer"))


        def _parse_baseline(data: object) -> Union['AssaysSummarizeJsonBodyBaselineType0', 'AssaysSummarizeJsonBodyBaselineType1', 'AssaysSummarizeJsonBodyBaselineType2']:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                baseline_type_0 = AssaysSummarizeJsonBodyBaselineType0.from_dict(data)



                return baseline_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                baseline_type_1 = AssaysSummarizeJsonBodyBaselineType1.from_dict(data)



                return baseline_type_1
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            baseline_type_2 = AssaysSummarizeJsonBodyBaselineType2.from_dict(data)



            return baseline_type_2

        baseline = _parse_baseline(d.pop("baseline"))


        assays_summarize_json_body = cls(
            summarizer=summarizer,
            baseline=baseline,
        )

        assays_summarize_json_body.additional_properties = d
        return assays_summarize_json_body

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
