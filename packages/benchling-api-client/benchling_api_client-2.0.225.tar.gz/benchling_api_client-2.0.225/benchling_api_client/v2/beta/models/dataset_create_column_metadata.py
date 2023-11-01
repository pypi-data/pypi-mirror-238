from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.dataset_column_type_metadata import DatasetColumnTypeMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetCreateColumnMetadata")


@attr.s(auto_attribs=True, repr=False)
class DatasetCreateColumnMetadata:
    """  """

    _type: DatasetColumnTypeMetadata
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DatasetCreateColumnMetadata({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> DatasetColumnTypeMetadata:
            type = DatasetColumnTypeMetadata.from_dict(d.pop("type"), strict=False)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(DatasetColumnTypeMetadata, UNSET)

        dataset_create_column_metadata = cls(
            type=type,
        )

        dataset_create_column_metadata.additional_properties = d
        return dataset_create_column_metadata

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def type(self) -> DatasetColumnTypeMetadata:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: DatasetColumnTypeMetadata) -> None:
        self._type = value
