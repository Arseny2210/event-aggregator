"""ImportJob ORM model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDMixin
from app.models.enums import ImportStatus

if TYPE_CHECKING:
    from app.models.user import User


class ImportJob(UUIDMixin, Base):
    """Stores Excel import history."""

    __tablename__ = "import_jobs"

    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    imported_rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    failed_rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    status: Mapped[ImportStatus] = mapped_column(
        Enum(
            ImportStatus,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        default=ImportStatus.processing,
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    created_by_user: Mapped[User] = relationship(
        back_populates="import_jobs",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<ImportJob(id={self.id}, filename={self.filename!r})>"
