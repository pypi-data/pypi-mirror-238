from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceCategory")


@_attrs_define
class ResourceCategory:
    """
    Attributes:
        name (str):
        mnemonic (str):
        category_type (str):
    """

    name: str
    mnemonic: str
    category_type: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        category_type = self.category_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "category_type": category_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        category_type = d.pop("category_type")

        resource_category = cls(
            name=name,
            mnemonic=mnemonic,
            category_type=category_type,
        )

        resource_category.additional_properties = d
        return resource_category

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
