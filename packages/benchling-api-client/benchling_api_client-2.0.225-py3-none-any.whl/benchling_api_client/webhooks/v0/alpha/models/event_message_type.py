from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EventMessageType(Enums.KnownString):
    V0_ALPHAEVENTCREATED = "v0-alpha.event.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EventMessageType":
        if not isinstance(val, str):
            raise ValueError(f"Value of EventMessageType must be a string (encountered: {val})")
        newcls = Enum("EventMessageType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EventMessageType, getattr(newcls, "_UNKNOWN"))
