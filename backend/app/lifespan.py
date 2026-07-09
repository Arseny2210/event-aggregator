import asyncio
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import async_session_factory, engine
from app.services.cleanup_worker import CleanupWorker
from app.services.scheduled_notification_worker import ScheduledNotificationWorker

logger = getLogger(__name__)

_scheduled_task: asyncio.Task | None = None
_cleanup_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduled_task, _cleanup_task

    logger.info("Application startup")
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await conn.commit()
        logger.info("Database connection verified")
    except Exception as exc:
        logger.warning("Database connection check failed: %s", exc)

    scheduled_worker = ScheduledNotificationWorker(async_session_factory, interval=15)
    cleanup_worker = CleanupWorker(async_session_factory, retention_days=7, interval=3600)

    _scheduled_task = asyncio.create_task(scheduled_worker.start())
    _cleanup_task = asyncio.create_task(cleanup_worker.start())
    logger.info("Background workers started")

    yield

    logger.info("Application shutdown")
    await scheduled_worker.stop()
    await cleanup_worker.stop()
    if _scheduled_task is not None:
        _scheduled_task.cancel()
    if _cleanup_task is not None:
        _cleanup_task.cancel()
    await engine.dispose()
