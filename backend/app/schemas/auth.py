"""Authentication DTOs."""

import uuid
from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema


class LoginRequest(BaseSchema):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8)


class RefreshTokenRequest(BaseSchema):
    refresh_token: str


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RoleInfo(BaseSchema):
    id: int
    name: str


class UserMeResponse(BaseSchema):
    id: uuid.UUID
    username: str
    email: EmailStr
    role: RoleInfo
    is_active: bool
    last_login: datetime | None = Field(default=None)
    created_at: datetime
    updated_at: datetime
    permissions: list[str] = Field(default_factory=list)
