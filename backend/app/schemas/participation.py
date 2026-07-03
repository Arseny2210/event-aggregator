"""Participation DTOs."""

import uuid
from datetime import datetime

from pydantic import Field

from app.models.enums import ParticipationStatus
from app.schemas.base import BaseSchema


class ParticipationCreate(BaseSchema):
    event_id: uuid.UUID
    session_id: str = Field(min_length=1, max_length=255)


class ParticipationResponse(BaseSchema):
    id: uuid.UUID
    event_id: uuid.UUID
    session_id: str
    status: ParticipationStatus
    created_at: datetime
