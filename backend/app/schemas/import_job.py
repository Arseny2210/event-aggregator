"""ImportJob DTOs."""

import uuid
from datetime import datetime

from pydantic import Field, computed_field

from app.models.enums import ImportStatus
from app.schemas.base import BaseSchema


class ImportSummary(BaseSchema):
    total_rows: int = Field(ge=0)
    processed_rows: int = Field(ge=0)
    imported_rows: int = Field(ge=0)
    failed_rows: int = Field(ge=0)
    warning_rows: int = Field(ge=0)
    duration: int = Field(ge=0)
    started_at: datetime | None = None
    finished_at: datetime | None = None

    @computed_field
    @property
    def progress_percent(self) -> float:
        if self.total_rows == 0:
            return 0.0
        return round(self.processed_rows / self.total_rows * 100, 2)


class ImportJobResponse(BaseSchema):
    id: uuid.UUID
    filename: str = Field(max_length=500)
    status: ImportStatus
    created_by: uuid.UUID
    created_at: datetime
    summary: ImportSummary
