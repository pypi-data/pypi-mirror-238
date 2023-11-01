from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.event_message_type import EventMessageType
from ..models.v2_assay_run_created_event import V2AssayRunCreatedEvent
from ..models.v2_assay_run_updated_fields_event import V2AssayRunUpdatedFieldsEvent
from ..models.v2_entity_registered_event import V2EntityRegisteredEvent
from ..models.v2_entry_created_event import V2EntryCreatedEvent
from ..models.v2_entry_updated_fields_event import V2EntryUpdatedFieldsEvent
from ..models.v2_entry_updated_review_record_event import V2EntryUpdatedReviewRecordEvent
from ..models.v2_request_created_event import V2RequestCreatedEvent
from ..models.v2_request_updated_fields_event import V2RequestUpdatedFieldsEvent
from ..models.v2_request_updated_status_event import V2RequestUpdatedStatusEvent
from ..models.v2_workflow_output_created_event import V2WorkflowOutputCreatedEvent
from ..models.v2_workflow_output_updated_fields_event import V2WorkflowOutputUpdatedFieldsEvent
from ..models.v2_workflow_task_created_event import V2WorkflowTaskCreatedEvent
from ..models.v2_workflow_task_group_created_event import V2WorkflowTaskGroupCreatedEvent
from ..models.v2_workflow_task_group_updated_watchers_event import V2WorkflowTaskGroupUpdatedWatchersEvent
from ..models.v2_workflow_task_updated_assignee_event import V2WorkflowTaskUpdatedAssigneeEvent
from ..models.v2_workflow_task_updated_fields_event import V2WorkflowTaskUpdatedFieldsEvent
from ..models.v2_workflow_task_updated_scheduled_on_event import V2WorkflowTaskUpdatedScheduledOnEvent
from ..models.v2_workflow_task_updated_status_event import V2WorkflowTaskUpdatedStatusEvent
from ..types import UNSET, Unset

T = TypeVar("T", bound="EventMessage")


@attr.s(auto_attribs=True, repr=False)
class EventMessage:
    """  """

    _event: Union[
        Unset,
        V2AssayRunCreatedEvent,
        V2AssayRunUpdatedFieldsEvent,
        V2EntityRegisteredEvent,
        V2EntryCreatedEvent,
        V2EntryUpdatedFieldsEvent,
        V2EntryUpdatedReviewRecordEvent,
        V2RequestCreatedEvent,
        V2RequestUpdatedFieldsEvent,
        V2RequestUpdatedStatusEvent,
        V2WorkflowTaskGroupCreatedEvent,
        V2WorkflowTaskGroupUpdatedWatchersEvent,
        V2WorkflowTaskCreatedEvent,
        V2WorkflowTaskUpdatedAssigneeEvent,
        V2WorkflowTaskUpdatedScheduledOnEvent,
        V2WorkflowTaskUpdatedStatusEvent,
        V2WorkflowTaskUpdatedFieldsEvent,
        V2WorkflowOutputCreatedEvent,
        V2WorkflowOutputUpdatedFieldsEvent,
        UnknownType,
    ] = UNSET
    _type: Union[Unset, EventMessageType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("event={}".format(repr(self._event)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EventMessage({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        event: Union[Unset, Dict[str, Any]]
        if isinstance(self._event, Unset):
            event = UNSET
        elif isinstance(self._event, UnknownType):
            event = self._event.value
        elif isinstance(self._event, V2AssayRunCreatedEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2AssayRunUpdatedFieldsEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2EntityRegisteredEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2EntryCreatedEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2EntryUpdatedFieldsEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2EntryUpdatedReviewRecordEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2RequestCreatedEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2RequestUpdatedFieldsEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2RequestUpdatedStatusEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowTaskGroupCreatedEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowTaskGroupUpdatedWatchersEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowTaskCreatedEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowTaskUpdatedAssigneeEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowTaskUpdatedScheduledOnEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowTaskUpdatedStatusEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowTaskUpdatedFieldsEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        elif isinstance(self._event, V2WorkflowOutputCreatedEvent):
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        else:
            event = UNSET
            if not isinstance(self._event, Unset):
                event = self._event.to_dict()

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if event is not UNSET:
            field_dict["event"] = event
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_event() -> Union[
            Unset,
            V2AssayRunCreatedEvent,
            V2AssayRunUpdatedFieldsEvent,
            V2EntityRegisteredEvent,
            V2EntryCreatedEvent,
            V2EntryUpdatedFieldsEvent,
            V2EntryUpdatedReviewRecordEvent,
            V2RequestCreatedEvent,
            V2RequestUpdatedFieldsEvent,
            V2RequestUpdatedStatusEvent,
            V2WorkflowTaskGroupCreatedEvent,
            V2WorkflowTaskGroupUpdatedWatchersEvent,
            V2WorkflowTaskCreatedEvent,
            V2WorkflowTaskUpdatedAssigneeEvent,
            V2WorkflowTaskUpdatedScheduledOnEvent,
            V2WorkflowTaskUpdatedStatusEvent,
            V2WorkflowTaskUpdatedFieldsEvent,
            V2WorkflowOutputCreatedEvent,
            V2WorkflowOutputUpdatedFieldsEvent,
            UnknownType,
        ]:
            event: Union[
                Unset,
                V2AssayRunCreatedEvent,
                V2AssayRunUpdatedFieldsEvent,
                V2EntityRegisteredEvent,
                V2EntryCreatedEvent,
                V2EntryUpdatedFieldsEvent,
                V2EntryUpdatedReviewRecordEvent,
                V2RequestCreatedEvent,
                V2RequestUpdatedFieldsEvent,
                V2RequestUpdatedStatusEvent,
                V2WorkflowTaskGroupCreatedEvent,
                V2WorkflowTaskGroupUpdatedWatchersEvent,
                V2WorkflowTaskCreatedEvent,
                V2WorkflowTaskUpdatedAssigneeEvent,
                V2WorkflowTaskUpdatedScheduledOnEvent,
                V2WorkflowTaskUpdatedStatusEvent,
                V2WorkflowTaskUpdatedFieldsEvent,
                V2WorkflowOutputCreatedEvent,
                V2WorkflowOutputUpdatedFieldsEvent,
                UnknownType,
            ]
            _event = d.pop("event")

            if not isinstance(_event, Unset):
                discriminator = _event["eventType"]
                if discriminator == "v2.assayRun.created":
                    event = V2AssayRunCreatedEvent.from_dict(_event)
                elif discriminator == "v2.assayRun.updated.fields":
                    event = V2AssayRunUpdatedFieldsEvent.from_dict(_event)
                elif discriminator == "v2.entity.registered":
                    event = V2EntityRegisteredEvent.from_dict(_event)
                elif discriminator == "v2.entry.created":
                    event = V2EntryCreatedEvent.from_dict(_event)
                elif discriminator == "v2.entry.updated.fields":
                    event = V2EntryUpdatedFieldsEvent.from_dict(_event)
                elif discriminator == "v2.entry.updated.reviewRecord":
                    event = V2EntryUpdatedReviewRecordEvent.from_dict(_event)
                elif discriminator == "v2.request.created":
                    event = V2RequestCreatedEvent.from_dict(_event)
                elif discriminator == "v2.request.updated.fields":
                    event = V2RequestUpdatedFieldsEvent.from_dict(_event)
                elif discriminator == "v2.request.updated.status":
                    event = V2RequestUpdatedStatusEvent.from_dict(_event)
                elif discriminator == "v2.workflowOutput.created":
                    event = V2WorkflowOutputCreatedEvent.from_dict(_event)
                elif discriminator == "v2.workflowOutput.updated.fields":
                    event = V2WorkflowOutputUpdatedFieldsEvent.from_dict(_event)
                elif discriminator == "v2.workflowTask.created":
                    event = V2WorkflowTaskCreatedEvent.from_dict(_event)
                elif discriminator == "v2.workflowTask.updated.assignee":
                    event = V2WorkflowTaskUpdatedAssigneeEvent.from_dict(_event)
                elif discriminator == "v2.workflowTask.updated.fields":
                    event = V2WorkflowTaskUpdatedFieldsEvent.from_dict(_event)
                elif discriminator == "v2.workflowTask.updated.scheduledOn":
                    event = V2WorkflowTaskUpdatedScheduledOnEvent.from_dict(_event)
                elif discriminator == "v2.workflowTask.updated.status":
                    event = V2WorkflowTaskUpdatedStatusEvent.from_dict(_event)
                elif discriminator == "v2.workflowTaskGroup.created":
                    event = V2WorkflowTaskGroupCreatedEvent.from_dict(_event)
                elif discriminator == "v2.workflowTaskGroup.updated.watchers":
                    event = V2WorkflowTaskGroupUpdatedWatchersEvent.from_dict(_event)
                else:
                    event = UnknownType(value=_event)

            return event

        try:
            event = get_event()
        except KeyError:
            if strict:
                raise
            event = cast(
                Union[
                    Unset,
                    V2AssayRunCreatedEvent,
                    V2AssayRunUpdatedFieldsEvent,
                    V2EntityRegisteredEvent,
                    V2EntryCreatedEvent,
                    V2EntryUpdatedFieldsEvent,
                    V2EntryUpdatedReviewRecordEvent,
                    V2RequestCreatedEvent,
                    V2RequestUpdatedFieldsEvent,
                    V2RequestUpdatedStatusEvent,
                    V2WorkflowTaskGroupCreatedEvent,
                    V2WorkflowTaskGroupUpdatedWatchersEvent,
                    V2WorkflowTaskCreatedEvent,
                    V2WorkflowTaskUpdatedAssigneeEvent,
                    V2WorkflowTaskUpdatedScheduledOnEvent,
                    V2WorkflowTaskUpdatedStatusEvent,
                    V2WorkflowTaskUpdatedFieldsEvent,
                    V2WorkflowOutputCreatedEvent,
                    V2WorkflowOutputUpdatedFieldsEvent,
                    UnknownType,
                ],
                UNSET,
            )

        def get_type() -> Union[Unset, EventMessageType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = EventMessageType(_type)
                except ValueError:
                    type = EventMessageType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, EventMessageType], UNSET)

        event_message = cls(
            event=event,
            type=type,
        )

        event_message.additional_properties = d
        return event_message

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
    def event(
        self,
    ) -> Union[
        V2AssayRunCreatedEvent,
        V2AssayRunUpdatedFieldsEvent,
        V2EntityRegisteredEvent,
        V2EntryCreatedEvent,
        V2EntryUpdatedFieldsEvent,
        V2EntryUpdatedReviewRecordEvent,
        V2RequestCreatedEvent,
        V2RequestUpdatedFieldsEvent,
        V2RequestUpdatedStatusEvent,
        V2WorkflowTaskGroupCreatedEvent,
        V2WorkflowTaskGroupUpdatedWatchersEvent,
        V2WorkflowTaskCreatedEvent,
        V2WorkflowTaskUpdatedAssigneeEvent,
        V2WorkflowTaskUpdatedScheduledOnEvent,
        V2WorkflowTaskUpdatedStatusEvent,
        V2WorkflowTaskUpdatedFieldsEvent,
        V2WorkflowOutputCreatedEvent,
        V2WorkflowOutputUpdatedFieldsEvent,
        UnknownType,
    ]:
        if isinstance(self._event, Unset):
            raise NotPresentError(self, "event")
        return self._event

    @event.setter
    def event(
        self,
        value: Union[
            V2AssayRunCreatedEvent,
            V2AssayRunUpdatedFieldsEvent,
            V2EntityRegisteredEvent,
            V2EntryCreatedEvent,
            V2EntryUpdatedFieldsEvent,
            V2EntryUpdatedReviewRecordEvent,
            V2RequestCreatedEvent,
            V2RequestUpdatedFieldsEvent,
            V2RequestUpdatedStatusEvent,
            V2WorkflowTaskGroupCreatedEvent,
            V2WorkflowTaskGroupUpdatedWatchersEvent,
            V2WorkflowTaskCreatedEvent,
            V2WorkflowTaskUpdatedAssigneeEvent,
            V2WorkflowTaskUpdatedScheduledOnEvent,
            V2WorkflowTaskUpdatedStatusEvent,
            V2WorkflowTaskUpdatedFieldsEvent,
            V2WorkflowOutputCreatedEvent,
            V2WorkflowOutputUpdatedFieldsEvent,
            UnknownType,
        ],
    ) -> None:
        self._event = value

    @event.deleter
    def event(self) -> None:
        self._event = UNSET

    @property
    def type(self) -> EventMessageType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: EventMessageType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
