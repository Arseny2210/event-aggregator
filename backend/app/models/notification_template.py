"""NotificationTemplate ORM model."""

from __future__ import annotations

from sqlalchemy import Boolean, Enum, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import NotificationChannelType, NotificationTemplateType


class NotificationTemplate(UUIDMixin, TimestampMixin, Base):
    """Stores reusable notification templates with versioning.

    Unique per (template_type, channel, language, version).
    """

    __tablename__ = "notification_templates"
    __table_args__ = (
        UniqueConstraint(
            "template_type",
            "channel",
            "language",
            "version",
            name="uq_template_type_channel_lang_ver",
        ),
    )

    template_type: Mapped[NotificationTemplateType] = mapped_column(
        Enum(
            NotificationTemplateType,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )
    channel: Mapped[NotificationChannelType] = mapped_column(
        Enum(
            NotificationChannelType,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )
    subject: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        default=None,
    )
    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
    )
    language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="en",
        server_default="en",
    )

    def __repr__(self) -> str:
        return (
            f"<NotificationTemplate(id={self.id}, "
            f"type={self.template_type.value!r}, channel={self.channel.value!r}, "
            f"lang={self.language!r}, v{self.version})>"
        )
