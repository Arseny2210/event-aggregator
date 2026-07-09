"""Notification ORM model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, UUIDMixin
from app.models.enums import (
    NotificationChannelType,
    NotificationPriority,
    NotificationStatus,
    NotificationTemplateType,
)


class Notification(UUIDMixin, Base):
    """Persistent notification history and queue."""

    __tablename__ = "notifications"

    channel: Mapped[NotificationChannelType] = mapped_column(
        Enum(
            NotificationChannelType,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )
    recipient: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    template_type: Mapped[NotificationTemplateType] = mapped_column(
        Enum(
            NotificationTemplateType,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )
    payload: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    subject: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        default=None,
    )
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(
            NotificationStatus,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        default=NotificationStatus.pending,
    )
    priority: Mapped[NotificationPriority] = mapped_column(
        Enum(
            NotificationPriority,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        default=NotificationPriority.NORMAL,
    )
    attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    max_retries: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
        server_default="3",
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        default=None,
    )

    def __repr__(self) -> str:
        return (
            f"<Notification(id={self.id}, channel={self.channel.value!r}, "
            f"status={self.status.value!r})>"
        )
