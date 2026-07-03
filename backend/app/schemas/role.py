"""Role DTOs."""

from pydantic import Field

from app.schemas.base import BaseSchema


class RoleResponse(BaseSchema):
    id: int
    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=10000)
