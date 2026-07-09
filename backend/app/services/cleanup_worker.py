"""CleanupWorker — periodic removal of old in-app notifications (7-day retention)."""

from __future__ import annotations

import asyncio
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.repositories.notification import NotificationRepository

logger = getLogger(__name__)


class CleanupWorker:
    """Periodically soft-deletes old in-app notifications."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        retention_days: int = 7,
        interval: int = 3600,
    ) -> None:
        self._session_factory = session_factory
        self._retention_days = retention_days
        self._interval = interval
        self._running = False

    async def start(self) -> None:
        self._running = True
        logger.info(
            "CleanupWorker started (retention=%dd, interval=%ds)",
            self._retention_days,
            self._interval,
        )
        while self._running:
            try:
                await self._cleanup()
            except Exception:
                logger.exception("CleanupWorker iteration failed")
            await asyncio.sleep(self._interval)

    async def stop(self) -> None:
        self._running = False
        logger.info("CleanupWorker stopped")

    async def _cleanup(self) -> None:
        async with self._session_factory() as session:
            repo = NotificationRepository(session)
            deleted = await repo.cleanup_old_notifications(days=self._retention_days)
            if deleted:
                await session.commit()
                logger.info("CleanupWorker: soft-deleted %d old notifications", deleted)
