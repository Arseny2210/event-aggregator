"""ScheduledNotificationWorker — background process for delivering scheduled in-app notifications.

Runs in a background asyncio task, processing pending notifications whose
scheduled_at has elapsed.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.enums import NotificationStatus
from app.repositories.notification import NotificationRepository

logger = getLogger(__name__)


class ScheduledNotificationWorker:
    """Periodically checks for and delivers scheduled in-app notifications."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        interval: int = 60,
    ) -> None:
        self._session_factory = session_factory
        self._interval = interval
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        self._running = True
        logger.info("ScheduledNotificationWorker started (interval=%ds)", self._interval)
        while self._running:
            try:
                await self._process_scheduled()
            except Exception:
                logger.exception("ScheduledNotificationWorker iteration failed")
            await asyncio.sleep(self._interval)

    async def stop(self) -> None:
        self._running = False
        logger.info("ScheduledNotificationWorker stopped")

    async def _process_scheduled(self) -> None:
        async with self._session_factory() as session:
            repo = NotificationRepository(session)
            notifications = await repo.get_pending_in_app(offset=0, limit=100)
            if not notifications:
                return
            now = datetime.now(UTC)
            for notification in notifications:
                notification.status = NotificationStatus.sent
                notification.sent_at = now
            await session.commit()
            logger.info(
                "ScheduledNotificationWorker: delivered %d notifications", len(notifications)
            )
