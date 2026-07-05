"""Category DTOs."""

import uuid

from app.schemas.base import BaseSchema


class CategoryResponse(BaseSchema):
    id: uuid.UUID
    name: str
    description: str | None = None
