"""Notification DTOs — NotificationContext dataclass and Pydantic response schemas."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import Field

from app.models.enums import (
    NotificationChannelType,
    NotificationPriority,
    NotificationStatus,
    NotificationTemplateType,
)
from app.schemas.base import BaseSchema


@dataclass(frozen=True, slots=True)
class NotificationContext:
    """Typed context for notification template rendering.

    Domain-specific fields plus an extensible `extra` dict.
    Specialized contexts (e.g. EventReminderContext) subclass this base.
    """

    event_title: str | None = None
    event_id: UUID | None = None
    event_start_date: date | None = None
    user_name: str | None = None
    user_email: str | None = None
    import_job_id: UUID | None = None
    import_filename: str | None = None
    import_total_rows: int | None = None
    import_imported_rows: int | None = None
    import_failed_rows: int | None = None
    organizer_name: str | None = None
    custom_message: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_template_namespace(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "event_title": self.event_title,
            "event_id": str(self.event_id) if self.event_id is not None else None,
            "event_start_date": self.event_start_date.isoformat()
            if self.event_start_date is not None
            else None,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "import_job_id": str(self.import_job_id) if self.import_job_id is not None else None,
            "import_filename": self.import_filename,
            "import_total_rows": self.import_total_rows,
            "import_imported_rows": self.import_imported_rows,
            "import_failed_rows": self.import_failed_rows,
            "organizer_name": self.organizer_name,
            "custom_message": self.custom_message,
        }
        result.update(self.extra)
        return result


class NotificationResponse(BaseSchema):
    id: UUID
    channel: NotificationChannelType
    recipient: str
    template_type: NotificationTemplateType
    payload: dict[str, Any]
    subject: str | None
    status: NotificationStatus
    priority: NotificationPriority
    attempts: int
    error_message: str | None
    created_at: datetime
    sent_at: datetime | None
    scheduled_at: datetime | None
    read_at: datetime | None
    deleted_at: datetime | None
    event_id: UUID | None


class NotificationTemplateResponse(BaseSchema):
    id: UUID
    template_type: NotificationTemplateType
    channel: NotificationChannelType
    subject: str | None
    is_active: bool
    version: int
    language: str
    created_at: datetime
    updated_at: datetime


class SendNotificationRequest(BaseSchema):
    channel: NotificationChannelType
    recipient: str = Field(min_length=1, max_length=500)
    template_type: NotificationTemplateType
    priority: NotificationPriority = Field(default=NotificationPriority.NORMAL)
    context: dict[str, Any] = Field(default_factory=dict)
    language: str = Field(default="en", max_length=10)


class SendTestNotificationRequest(BaseSchema):
    channel: NotificationChannelType
    recipient: str = Field(min_length=1, max_length=500)
    template_type: NotificationTemplateType
    language: str = Field(default="en", max_length=10)
