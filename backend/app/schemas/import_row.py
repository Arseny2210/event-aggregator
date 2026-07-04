"""Internal validation schema for Excel row data.

This schema validates raw Excel row data before event creation.
It is NOT an API DTO — used only inside ImportProcessor.
"""

import uuid
from datetime import date, time

from pydantic import Field

from app.schemas.base import BaseSchema


class EventExcelRow(BaseSchema):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=10000)
    start_date: date
    start_time: time | None = None
    end_time: time | None = None
    location: str = Field(min_length=1, max_length=255)
    organizer_name: str = Field(min_length=1, max_length=255)
    short_description: str | None = Field(default=None, max_length=1000)
    image_url: str | None = Field(default=None, max_length=2000)
    registration_url: str | None = Field(default=None, max_length=2000)
    category_id: uuid.UUID | None = None
