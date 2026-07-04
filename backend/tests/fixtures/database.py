"""Database fixtures for test isolation.

Uses PostgreSQL test database with per-test transaction rollback.
Set TEST_DATABASE_URL env var to override.
Default uses Docker PostgreSQL on port 5435.
"""

import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.database.base import Base

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5435/event_aggregator_test",
)

_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, pool_pre_ping=True)
_tables_created = False


async def _ensure_tables():
    global _tables_created
    if _tables_created:
        return
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    _tables_created = True


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Per-test session with transaction rollback."""
    await _ensure_tables()
    conn = await _engine.connect()
    transaction = await conn.begin()
    session = AsyncSession(
        bind=conn,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await conn.close()
