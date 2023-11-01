from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.images_images import ImagesImages





T = TypeVar("T", bound="Images")


@attr.s(auto_attribs=True)
class Images:
    """ 
        Attributes:
            images (Union[Unset, None, ImagesImages]):
     """

    images: Union[Unset, None, 'ImagesImages'] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        images: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.images, Unset):
            images = self.images.to_dict() if self.images else None


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if images is not UNSET:
            field_dict["images"] = images

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.images_images import ImagesImages
        d = src_dict.copy()
        _images = d.pop("images", UNSET)
        images: Union[Unset, None, ImagesImages]
        if _images is None:
            images = None
        elif isinstance(_images,  Unset):
            images = UNSET
        else:
            images = ImagesImages.from_dict(_images)




        images = cls(
            images=images,
        )

        images.additional_properties = d
        return images

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
