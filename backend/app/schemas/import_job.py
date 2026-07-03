"""ImportJob DTOs."""

import uuid
from datetime import datetime

from pydantic import Field

from app.models.enums import ImportStatus
from app.schemas.base import BaseSchema


class ImportJobResponse(BaseSchema):
    id: uuid.UUID
    filename: str = Field(max_length=500)
    imported_rows: int = Field(ge=0)
    failed_rows: int = Field(ge=0)
    duration: int = Field(ge=0)
    status: ImportStatus
    created_by: uuid.UUID
    created_at: datetime
