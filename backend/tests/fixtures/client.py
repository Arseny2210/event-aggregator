"""HTTP client fixtures for API tests."""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.dependencies.database import get_db
from app.main import create_app


@pytest_asyncio.fixture
async def async_client(db_session):
    """Async HTTP client against the FastAPI application."""
    app = create_app()

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
