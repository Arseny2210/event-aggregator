"""Event DTOs."""

import uuid
from datetime import date, time

from pydantic import Field

from app.models.enums import EventStatus
from app.schemas.base import BaseSchema, TimestampSchema
from app.schemas.category import CategoryResponse


class EventBase(BaseSchema):
    title: str = Field(min_length=1, max_length=255)
    short_description: str | None = Field(default=None, max_length=1000)
    description: str | None = Field(default=None, max_length=10000)
    start_date: date
    start_time: time | None = Field(default=None)
    end_time: time | None = Field(default=None)
    location: str = Field(min_length=1, max_length=255)
    image_url: str | None = Field(default=None, max_length=2000)
    registration_url: str | None = Field(default=None, max_length=2000)
    status: EventStatus = Field(default=EventStatus.draft)
    target_audience: str | None = Field(default=None, max_length=100)
    participation_enabled: bool = Field(default=True)


class EventCreate(EventBase):
    organizer_id: uuid.UUID
    category_id: uuid.UUID
    description: str = Field(min_length=1, max_length=10000)


class EventUpdate(BaseSchema):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    short_description: str | None = Field(default=None, max_length=1000)
    description: str | None = Field(default=None, max_length=10000)
    start_date: date | None = Field(default=None)
    start_time: time | None = Field(default=None)
    end_time: time | None = Field(default=None)
    location: str | None = Field(default=None, min_length=1, max_length=255)
    image_url: str | None = Field(default=None, max_length=2000)
    registration_url: str | None = Field(default=None, max_length=2000)
    status: EventStatus | None = Field(default=None)
    organizer_id: uuid.UUID | None = Field(default=None)
    category_id: uuid.UUID | None = Field(default=None)
    target_audience: str | None = Field(default=None, max_length=100)
    participation_enabled: bool | None = Field(default=None)


class EventResponse(EventBase, TimestampSchema):
    id: uuid.UUID
    organizer_id: uuid.UUID
    category_id: uuid.UUID
    category: CategoryResponse
    description: str = Field(max_length=10000)
    target_audience: str | None = None
    participants_count: int = 0
