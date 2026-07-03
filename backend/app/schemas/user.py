"""User DTOs."""

import uuid
from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema, TimestampSchema


class UserBase(BaseSchema):
    username: str = Field(min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr = Field(max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    role_id: int = Field(ge=1)


class UserUpdate(BaseSchema):
    username: str | None = Field(
        default=None, min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8)
    role_id: int | None = Field(default=None, ge=1)
    is_active: bool | None = Field(default=None)


class UserResponse(UserBase, TimestampSchema):
    id: uuid.UUID
    role_id: int
    is_active: bool
    last_login: datetime | None = Field(default=None)
