"""Notification repository."""

from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import NotificationChannelType, NotificationStatus
from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """Repository for Notification entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Notification)

    async def get_by_id(self, entity_id: UUID) -> Notification | None:
        statement = select(Notification).where(Notification.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[Notification]:
        statement = (
            select(Notification)
            .where(Notification.id.in_(ids))
            .order_by(Notification.created_at.desc())
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_status(
        self, status: NotificationStatus, offset: int, limit: int
    ) -> tuple[list[Notification], int]:
        statement = (
            select(Notification)
            .where(Notification.status == status)
            .order_by(Notification.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count()).select_from(Notification).where(Notification.status == status)
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_by_recipient(
        self, recipient: str, offset: int, limit: int
    ) -> tuple[list[Notification], int]:
        statement = (
            select(Notification)
            .where(Notification.recipient == recipient)
            .order_by(Notification.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count())
            .select_from(Notification)
            .where(Notification.recipient == recipient)
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_pending(self, offset: int, limit: int) -> list[Notification]:
        now = datetime.now(UTC)
        statement = (
            select(Notification)
            .where(
                Notification.status.in_((NotificationStatus.pending, NotificationStatus.retrying)),
                (Notification.scheduled_at.is_(None)) | (Notification.scheduled_at <= now),
            )
            .order_by(Notification.priority.desc(), Notification.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def update_status(
        self,
        notification_id: UUID,
        status: NotificationStatus,
        error_message: str | None = None,
        attempts: int | None = None,
        sent_at: datetime | None = None,
    ) -> Notification | None:
        notification = await self.get_by_id(notification_id)
        if notification is None:
            return None
        notification.status = status
        if error_message is not None:
            notification.error_message = error_message
        if attempts is not None:
            notification.attempts = attempts
        if sent_at is not None:
            notification.sent_at = sent_at
        await self.session.flush()
        return notification

    async def get_by_session_id(
        self, session_id: str, offset: int, limit: int
    ) -> tuple[list[Notification], int]:
        statement = (
            select(Notification)
            .where(
                Notification.recipient == session_id,
                Notification.channel == NotificationChannelType.in_app,
                Notification.deleted_at.is_(None),
            )
            .order_by(Notification.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count())
            .select_from(Notification)
            .where(
                Notification.recipient == session_id,
                Notification.channel == NotificationChannelType.in_app,
                Notification.deleted_at.is_(None),
            )
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_pending_in_app(self, offset: int, limit: int) -> list[Notification]:
        now = datetime.now(UTC)
        statement = (
            select(Notification)
            .where(
                Notification.channel == NotificationChannelType.in_app,
                Notification.status == NotificationStatus.pending,
                Notification.deleted_at.is_(None),
                or_(
                    Notification.scheduled_at.is_(None),
                    Notification.scheduled_at <= now,
                ),
            )
            .order_by(desc(Notification.priority), Notification.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: UUID) -> Notification | None:
        notification = await self.get_by_id(notification_id)
        if notification is None:
            return None
        notification.read_at = datetime.now(UTC)
        await self.session.flush()
        return notification

    async def soft_delete_notification(self, notification_id: UUID) -> Notification | None:
        notification = await self.get_by_id(notification_id)
        if notification is None:
            return None
        notification.deleted_at = datetime.now(UTC)
        await self.session.flush()
        return notification

    async def delete_by_session_and_event(self, session_id: str, event_id: UUID) -> int:
        stmt = (
            update(Notification)
            .where(
                Notification.recipient == session_id,
                Notification.event_id == event_id,
                Notification.status == NotificationStatus.pending,
                Notification.deleted_at.is_(None),
            )
            .values(deleted_at=datetime.now(UTC))
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def cleanup_old_notifications(self, days: int = 7) -> int:
        cutoff = datetime.now(UTC) - timedelta(days=days)
        stmt = (
            update(Notification)
            .where(
                Notification.channel == NotificationChannelType.in_app,
                Notification.created_at < cutoff,
                Notification.deleted_at.is_(None),
            )
            .values(deleted_at=datetime.now(UTC))
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount
