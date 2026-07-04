"""Service for managing events and their lifecycle transitions."""

from datetime import date, time
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from app.models.enums import EventStatus
from app.models.event import Event
from app.repositories.event import EventRepository
from app.repositories.organizer import OrganizerRepository
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.schemas.event_search import EventSearchFilters
from app.schemas.page import Page
from app.services.exceptions import (
    ArchivedEventNotEditableError,
    EventNotFoundError,
    EventNotPublishableError,
    InvalidEventDataError,
    InvalidEventStatusTransitionError,
    OrganizerNotFoundError,
)
from app.services.transaction import transactional

_ALLOWED_TRANSITIONS: dict[EventStatus, frozenset[EventStatus]] = {
    EventStatus.draft: frozenset({EventStatus.published, EventStatus.draft}),
    EventStatus.published: frozenset({EventStatus.completed, EventStatus.published}),
    EventStatus.completed: frozenset({EventStatus.archived, EventStatus.completed}),
    EventStatus.archived: frozenset({EventStatus.archived}),
}


def _resolve_sort(sort_by: str | None) -> ColumnElement[Any]:
    if sort_by == "-date":
        return Event.start_date.desc()
    if sort_by == "title":
        return Event.title.asc()
    if sort_by == "-title":
        return Event.title.desc()
    if sort_by == "created_at":
        return Event.created_at.asc()
    if sort_by == "-created_at":
        return Event.created_at.desc()
    return Event.start_date.asc()


def _validate_times(start_time: time | None, end_time: time | None, event_id: UUID | None) -> None:
    if start_time is not None and end_time is not None and end_time <= start_time:
        raise InvalidEventDataError(event_id, "end_time must be after start_time")


class EventService:
    """Business logic for event management."""

    def __init__(
        self,
        session: AsyncSession,
        repository: EventRepository,
        organizer_repository: OrganizerRepository,
    ) -> None:
        self.session = session
        self.repository = repository
        self.organizer_repository = organizer_repository

    async def get_event(self, event_id: UUID) -> Event:
        event = await self.repository.get_by_id(event_id)
        if event is None:
            raise EventNotFoundError(event_id)
        return event

    async def create_event(self, data: EventCreate) -> Event:
        organizer = await self.organizer_repository.get_by_id(data.organizer_id)
        if organizer is None:
            raise OrganizerNotFoundError(data.organizer_id)
        _validate_times(data.start_time, data.end_time, None)
        async with transactional(self.session):
            event = Event(
                title=data.title,
                short_description=data.short_description,
                description=data.description,
                category_id=data.category_id,
                organizer_id=data.organizer_id,
                start_date=data.start_date,
                start_time=data.start_time,
                end_time=data.end_time,
                location=data.location,
                image_url=data.image_url,
                registration_url=data.registration_url,
                status=data.status,
            )
            return await self.repository.create(event)

    async def update_event(self, event_id: UUID, data: EventUpdate) -> Event:
        event = await self.get_event(event_id)
        if event.status == EventStatus.archived:
            raise ArchivedEventNotEditableError(event_id)
        payload = data.model_dump(exclude_unset=True)
        if "organizer_id" in payload and payload["organizer_id"] is not None:
            organizer = await self.organizer_repository.get_by_id(payload["organizer_id"])
            if organizer is None:
                raise OrganizerNotFoundError(payload["organizer_id"])
        new_start_time = payload.get("start_time", event.start_time)
        new_end_time = payload.get("end_time", event.end_time)
        _validate_times(new_start_time, new_end_time, event_id)
        if "status" in payload and payload["status"] is not None:
            self._validate_transition(event.status, payload["status"])
        async with transactional(self.session):
            for field, value in payload.items():
                setattr(event, field, value)
            return event

    async def delete_event(self, event_id: UUID) -> None:
        event = await self.get_event(event_id)
        async with transactional(self.session):
            await self.repository.delete(event)

    async def list_events(
        self, offset: int, limit: int, sort_by: str | None = None
    ) -> tuple[list[Event], int]:
        order_by = _resolve_sort(sort_by)
        return await self.repository.get_paginated(offset, limit, order_by)

    async def search_events(self, query: str, offset: int, limit: int) -> tuple[list[Event], int]:
        return await self.repository.search_by_title(query, offset, limit)

    async def search(
        self, filters: EventSearchFilters, offset: int, limit: int
    ) -> Page[EventResponse]:
        result = await self.repository.search(filters, offset, limit)
        return Page[EventResponse](
            items=[EventResponse.model_validate(e) for e in result.items],
            total=result.total,
            offset=offset,
            limit=limit,
        )

    async def list_events_by_organizer(
        self, organizer_id: UUID, offset: int, limit: int
    ) -> tuple[list[Event], int]:
        return await self.repository.get_by_organizer(organizer_id, offset, limit)

    async def list_events_by_status(
        self, status: EventStatus, offset: int, limit: int
    ) -> tuple[list[Event], int]:
        return await self.repository.get_by_status(status, offset, limit)

    async def list_events_by_date_range(
        self, start: date, end: date, offset: int, limit: int
    ) -> tuple[list[Event], int]:
        return await self.repository.get_by_date_range(start, end, offset, limit)

    async def publish_event(self, event_id: UUID) -> Event:
        event = await self.get_event(event_id)
        self._validate_transition(event.status, EventStatus.published)
        if event.start_date < date.today():
            raise EventNotPublishableError(event_id, "start_date is in the past")
        async with transactional(self.session):
            event.status = EventStatus.published
            return event

    async def complete_event(self, event_id: UUID) -> Event:
        event = await self.get_event(event_id)
        self._validate_transition(event.status, EventStatus.completed)
        async with transactional(self.session):
            event.status = EventStatus.completed
            return event

    async def archive_event(self, event_id: UUID) -> Event:
        event = await self.get_event(event_id)
        self._validate_transition(event.status, EventStatus.archived)
        async with transactional(self.session):
            event.status = EventStatus.archived
            return event

    @staticmethod
    def _validate_transition(current: EventStatus, attempted: EventStatus) -> None:
        allowed = _ALLOWED_TRANSITIONS.get(current, frozenset())
        if attempted not in allowed:
            raise InvalidEventStatusTransitionError(current, attempted)
