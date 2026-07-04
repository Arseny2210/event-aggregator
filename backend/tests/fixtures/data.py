"""Pre-built test data fixtures for quick test setup."""

import pytest_asyncio

from app.models.enums import EventStatus
from tests.factories import EventFactory, OrganizerFactory, UserFactory


@pytest_asyncio.fixture
async def sample_organizer(db_session):
    return await OrganizerFactory.create(db_session, name="Sample Organizer")


@pytest_asyncio.fixture
async def sample_event(db_session, sample_organizer):
    return await EventFactory.create(
        db_session,
        title="Sample Event",
        organizer=sample_organizer,
        status=EventStatus.draft,
    )


@pytest_asyncio.fixture
async def sample_user(db_session):
    return await UserFactory.create(db_session, username="sample_user")
