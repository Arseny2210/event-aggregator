"""Organizer ORM model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.event import Event


class Organizer(UUIDMixin, TimestampMixin, Base):
    """Stores event organizers."""

    __tablename__ = "organizers"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    department: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )
    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None,
    )
    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        default=None,
    )

    events: Mapped[list[Event]] = relationship(
        back_populates="organizer",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Organizer(id={self.id}, name={self.name!r})>"
