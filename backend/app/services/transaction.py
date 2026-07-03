"""Reusable transactional context manager for service-layer write operations.

Usage inside a service method::

    async with transactional(self.session):
        result = await self.repository.create(entity)
        return result  # commit happens on clean exit

If any exception escapes the ``yield``, the session is rolled back before
the exception propagates.
"""

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
