"""Category DTOs."""

import uuid

from pydantic import Field

from app.schemas.base import BaseSchema


class CategoryCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CategoryResponse(BaseSchema):
    id: uuid.UUID
    name: str
    description: str | None = None
