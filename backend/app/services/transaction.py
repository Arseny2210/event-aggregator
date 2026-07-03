"""Reusable transactional context manager for service-layer write operations."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def transactional(session: AsyncSession) -> AsyncIterator[None]:
    try:
        yield
        await session.commit()
    except Exception:
        await session.rollback()
        raise
