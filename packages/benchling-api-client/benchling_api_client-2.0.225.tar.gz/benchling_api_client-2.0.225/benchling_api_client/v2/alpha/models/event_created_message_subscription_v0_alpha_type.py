from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class EventCreatedMessageSubscriptionV0AlphaType(Enums.KnownString):
    V0_ALPHAEVENTCREATED = "v0-alpha.event.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "EventCreatedMessageSubscriptionV0AlphaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of EventCreatedMessageSubscriptionV0AlphaType must be a string (encountered: {val})"
            )
        newcls = Enum("EventCreatedMessageSubscriptionV0AlphaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(EventCreatedMessageSubscriptionV0AlphaType, getattr(newcls, "_UNKNOWN"))
