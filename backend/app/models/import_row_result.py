"""ImportJobRowResult ORM model — per-row results for import jobs."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDMixin
from app.models.enums import ImportRowStatus

if TYPE_CHECKING:
    from app.models.import_job import ImportJob


class ImportJobRowResult(UUIDMixin, Base):
    """Per-row result of an Excel import job."""

    __tablename__ = "import_row_results"

    import_job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("import_jobs.id", ondelete="CASCADE"),
        nullable=False,
    )
    row_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    status: Mapped[ImportRowStatus] = mapped_column(
        Enum(
            ImportRowStatus,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )
    created_entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        default=None,
    )
    error_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        default=None,
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

    import_job: Mapped[ImportJob] = relationship(
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<ImportJobRowResult(id={self.id}, import_job_id={self.import_job_id}, "
            f"row={self.row_number}, status={self.status.value!r})>"
        )
