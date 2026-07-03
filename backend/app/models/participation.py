"""Participation ORM model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDMixin
from app.models.enums import ParticipationStatus

if TYPE_CHECKING:
    from app.models.event import Event


class Participation(UUIDMixin, Base):
    """Stores visitor participation."""

    __tablename__ = "participations"
    __table_args__ = (UniqueConstraint("event_id", "session_id"),)

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    session_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[ParticipationStatus] = mapped_column(
        Enum(
            ParticipationStatus,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        default=ParticipationStatus.registered,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    event: Mapped[Event] = relationship(
        back_populates="participations",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Participation(id={self.id}, event_id={self.event_id})>"
