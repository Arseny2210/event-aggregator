"""Event DTOs."""

import uuid
from datetime import date, time

from pydantic import Field

from app.models.enums import EventStatus
from app.schemas.base import BaseSchema, TimestampSchema


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


class EventResponse(EventBase, TimestampSchema):
    id: uuid.UUID
    organizer_id: uuid.UUID
    category_id: uuid.UUID
    description: str = Field(max_length=10000)
