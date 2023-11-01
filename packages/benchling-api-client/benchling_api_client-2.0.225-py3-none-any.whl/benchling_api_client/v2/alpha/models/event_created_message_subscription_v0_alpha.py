from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.event_created_message_subscription_v0_alpha_type import (
    EventCreatedMessageSubscriptionV0AlphaType,
)
from ..models.event_message_event_type import EventMessageEventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EventCreatedMessageSubscriptionV0Alpha")


@attr.s(auto_attribs=True, repr=False)
class EventCreatedMessageSubscriptionV0Alpha:
    """  """

    _event_type: EventMessageEventType
    _type: EventCreatedMessageSubscriptionV0AlphaType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("event_type={}".format(repr(self._event_type)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EventCreatedMessageSubscriptionV0Alpha({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        event_type = self._event_type.value

        type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if event_type is not UNSET:
            field_dict["eventType"] = event_type
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_event_type() -> EventMessageEventType:
            _event_type = d.pop("eventType")
            try:
                event_type = EventMessageEventType(_event_type)
            except ValueError:
                event_type = EventMessageEventType.of_unknown(_event_type)

            return event_type

        try:
            event_type = get_event_type()
        except KeyError:
            if strict:
                raise
            event_type = cast(EventMessageEventType, UNSET)

        def get_type() -> EventCreatedMessageSubscriptionV0AlphaType:
            _type = d.pop("type")
            try:
                type = EventCreatedMessageSubscriptionV0AlphaType(_type)
            except ValueError:
                type = EventCreatedMessageSubscriptionV0AlphaType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(EventCreatedMessageSubscriptionV0AlphaType, UNSET)

        event_created_message_subscription_v0_alpha = cls(
            event_type=event_type,
            type=type,
        )

        event_created_message_subscription_v0_alpha.additional_properties = d
        return event_created_message_subscription_v0_alpha

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
    def event_type(self) -> EventMessageEventType:
        """ The event that the app is subscribed to. """
        if isinstance(self._event_type, Unset):
            raise NotPresentError(self, "event_type")
        return self._event_type

    @event_type.setter
    def event_type(self, value: EventMessageEventType) -> None:
        self._event_type = value

    @property
    def type(self) -> EventCreatedMessageSubscriptionV0AlphaType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: EventCreatedMessageSubscriptionV0AlphaType) -> None:
        self._type = value
