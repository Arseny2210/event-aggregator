"""Event ORM model."""

from __future__ import annotations

import uuid
from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import EventStatus

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.organizer import Organizer
    from app.models.participation import Participation


class Event(UUIDMixin, TimestampMixin, Base):
    """Stores all university events."""

    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    short_description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    organizer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizers.id", ondelete="RESTRICT"), nullable=False
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time | None] = mapped_column(nullable=True, default=None)
    end_time: Mapped[time | None] = mapped_column(nullable=True, default=None)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    registration_url: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, native_enum=False, validate_strings=True),
        nullable=False,
        default=EventStatus.draft,
    )
    target_audience: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    participation_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    category: Mapped[Category] = relationship(back_populates="events", lazy="selectin")
    organizer: Mapped[Organizer] = relationship(back_populates="events", lazy="selectin")
    participations: Mapped[list[Participation]] = relationship(
        back_populates="event", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, title={self.title!r})>"
