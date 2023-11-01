from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DatasetColumnTypeNameEnumName(Enums.KnownString):
    STRING = "String"
    INT = "Int"
    FLOAT = "Float"
    JSON = "JSON"
    DATETIME = "DateTime"
    DATE = "Date"
    BOOLEAN = "Boolean"
    OBJECTLINK = "ObjectLink"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DatasetColumnTypeNameEnumName":
        if not isinstance(val, str):
            raise ValueError(f"Value of DatasetColumnTypeNameEnumName must be a string (encountered: {val})")
        newcls = Enum("DatasetColumnTypeNameEnumName", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DatasetColumnTypeNameEnumName, getattr(newcls, "_UNKNOWN"))
