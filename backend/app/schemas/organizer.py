"""Organizer DTOs."""

import uuid

from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema, TimestampSchema


class OrganizerBase(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    department: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    website: str | None = Field(default=None, max_length=500)


class OrganizerCreate(OrganizerBase):
    pass


class OrganizerUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    department: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    website: str | None = Field(default=None, max_length=500)


class OrganizerResponse(OrganizerBase, TimestampSchema):
    id: uuid.UUID
