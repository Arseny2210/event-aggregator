"""add_notification_read_delete_event_fields

Revision ID: 2fb2ce85a26e
Revises: 6ac886fe184c
Create Date: 2026-07-09 01:03:47.909076

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "2fb2ce85a26e"
down_revision: Union[str, None] = "6ac886fe184c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "notifications",
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "notifications",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "notifications",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index(
        "ix_notifications_session_id",
        "notifications",
        ["recipient"],
        postgresql_where=sa.text("channel = 'in_app'"),
    )


def downgrade() -> None:
    op.drop_index("ix_notifications_session_id", table_name="notifications")
    op.drop_column("notifications", "event_id")
    op.drop_column("notifications", "deleted_at")
    op.drop_column("notifications", "read_at")
