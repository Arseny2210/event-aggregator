"""NotificationSender — framework-independent notification delivery worker.

No FastAPI, no Depends, no HTTP concepts.
Compatible with asyncio.create_task and future Celery workers.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from logging import getLogger
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.exceptions import NotificationDeliveryError
from app.core.notifications import NotificationChannel
from app.core.tasks import BackgroundTaskDispatcher
from app.models.enums import NotificationChannelType, NotificationStatus
from app.repositories.notification import NotificationRepository

logger = getLogger(__name__)


class NotificationSender:
    """Background worker that delivers a single notification with retries.

    Framework-independent: receives primitives and a session factory.
    Swappable for Celery without changes to NotificationService.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        channels: dict[NotificationChannelType, NotificationChannel],
        max_retries: int = 3,
    ) -> None:
        self._session_factory = session_factory
        self._channels = channels
        self._max_retries = max_retries

    async def process(self, notification_id: UUID) -> None:
        async with self._session_factory() as session:
            repo = NotificationRepository(session)
            notification = await repo.get_by_id(notification_id)
            if notification is None:
                logger.error("NotificationSender: notification %s not found", notification_id)
                return

            if notification.status not in (
                NotificationStatus.pending,
                NotificationStatus.retrying,
            ):
                logger.info(
                    "NotificationSender: notification %s already processed (status=%s)",
                    notification_id,
                    notification.status.value,
                )
                return

            channel = self._channels.get(notification.channel)
            if channel is None:
                logger.error(
                    "NotificationSender: no channel for type %s",
                    notification.channel.value,
                )
                await repo.update_status(
                    notification_id,
                    NotificationStatus.failed,
                    error_message=f"No channel configured for {notification.channel.value}",
                )
                await session.commit()
                return

            max_retries = min(notification.max_retries, self._max_retries)
            last_error: str | None = None

            for attempt in range(1, max_retries + 1):
                try:
                    await channel.send(
                        notification.recipient,
                        notification.subject,
                        notification.payload.get("rendered_body", ""),
                    )
                    await repo.update_status(
                        notification_id,
                        NotificationStatus.sent,
                        attempts=attempt,
                        sent_at=datetime.now(UTC),
                    )
                    await session.commit()
                    logger.info(
                        "NotificationSender: sent %s on attempt %d",
                        notification_id,
                        attempt,
                    )
                    return
                except NotificationDeliveryError as exc:
                    last_error = str(exc)
                    logger.warning(
                        "NotificationSender: attempt %d/%d failed for %s: %s",
                        attempt,
                        max_retries,
                        notification_id,
                        last_error,
                    )
                    await repo.update_status(
                        notification_id,
                        NotificationStatus.retrying,
                        error_message=last_error,
                        attempts=attempt,
                    )
                    await session.commit()
                    if attempt < max_retries:
                        backoff = 2**attempt
                        await asyncio.sleep(backoff)

            await repo.update_status(
                notification_id,
                NotificationStatus.failed,
                error_message=last_error,
                attempts=max_retries,
            )
            await session.commit()
            logger.error(
                "NotificationSender: all %d retries exhausted for %s",
                max_retries,
                notification_id,
            )


class NotificationSenderFactory:
    """Creates and dispatches NotificationSender instances.

    Encapsulates session_factory, channels, dispatcher, and max_retries.
    NotificationService never instantiates NotificationSender directly.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        channels: dict[NotificationChannelType, NotificationChannel],
        dispatcher: BackgroundTaskDispatcher,
        max_retries: int = 3,
    ) -> None:
        self._session_factory = session_factory
        self._channels = channels
        self._dispatcher = dispatcher
        self._max_retries = max_retries

    def dispatch_send(self, notification_id: UUID) -> None:
        sender = NotificationSender(
            session_factory=self._session_factory,
            channels=self._channels,
            max_retries=self._max_retries,
        )
        self._dispatcher.dispatch(sender.process(notification_id))
