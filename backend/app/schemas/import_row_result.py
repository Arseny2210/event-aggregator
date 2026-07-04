"""ImportRowResult DTOs."""

import uuid
from datetime import datetime

from pydantic import Field

from app.models.enums import ImportRowStatus
from app.schemas.base import BaseSchema


class RowResultResponse(BaseSchema):
    id: uuid.UUID
    import_job_id: uuid.UUID
    row_number: int = Field(ge=1)
    status: ImportRowStatus
    created_entity_id: uuid.UUID | None = None
    error_code: str | None = None
    error_message: str | None = None
    created_at: datetime
