"""ImportJob ORM model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
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
    file_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
        default=None,
    )
    total_rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    processed_rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    warning_rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    created_by_user: Mapped[User] = relationship(
        back_populates="import_jobs",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<ImportJob(id={self.id}, filename={self.filename!r})>"
