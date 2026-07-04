"""Root conftest: imports all fixtures for pytest collection."""

import asyncio

import pytest

from tests.fixtures.auth import (
    admin_client,
    admin_role,
    admin_user,
    auth_headers,
    simple_role,
    simple_user,
)
from tests.fixtures.client import async_client
from tests.fixtures.data import sample_event, sample_organizer, sample_user
from tests.fixtures.database import _engine, db_session


@pytest.fixture(scope="session")
def event_loop():
    """Create a session-scoped event loop for all async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def pytest_sessionfinish(session, exitstatus):
    """Clean up engine after all tests."""
    import asyncio

    async def _dispose():
        await _engine.dispose()

    try:
        loop = asyncio.get_event_loop()
        if not loop.is_closed():
            loop.run_until_complete(_dispose())
    except RuntimeError:
        pass


__all__ = [
    "admin_client",
    "admin_role",
    "admin_user",
    "async_client",
    "auth_headers",
    "db_session",
    "event_loop",
    "sample_event",
    "sample_organizer",
    "sample_user",
    "simple_role",
    "simple_user",
]
