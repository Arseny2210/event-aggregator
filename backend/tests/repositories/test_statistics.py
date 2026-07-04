"""Tests for StatisticsRepository aggregations."""

from datetime import UTC, datetime

import pytest

from app.models.enums import EventStatus
from app.repositories.statistics import StatisticsRepository
from tests.factories import (
    EventFactory,
    OrganizerFactory,
    ParticipationFactory,
)


class TestStatisticsRepository:
    @pytest.mark.asyncio
    async def test_count_events_by_status(self, db_session):
        await EventFactory.create(db_session, status=EventStatus.draft)
        await EventFactory.create(db_session, status=EventStatus.published)
        repo = StatisticsRepository(db_session)
        counts = await repo.count_events_by_status(None, None)
        status_map = {c.status: c.count for c in counts}
        assert status_map.get(EventStatus.draft) == 1
        assert status_map.get(EventStatus.published) == 1

    @pytest.mark.asyncio
    async def test_count_total_organizers(self, db_session):
        await OrganizerFactory.create(db_session)
        await OrganizerFactory.create(db_session)
        repo = StatisticsRepository(db_session)
        total = await repo.count_total_organizers(None, None)
        assert total == 2

    @pytest.mark.asyncio
    async def test_top_organizers(self, db_session):
        org = await OrganizerFactory.create(db_session)
        await EventFactory.create(db_session, organizer=org)
        await EventFactory.create(db_session, organizer=org)
        repo = StatisticsRepository(db_session)
        results = await repo.top_organizers_by_event_count(5, None, None)
        assert len(results) >= 1
        assert results[0].event_count >= 2

    @pytest.mark.asyncio
    async def test_count_total_users(self, db_session):
        from tests.factories import UserFactory

        await UserFactory.create(db_session)
        await UserFactory.create(db_session)
        repo = StatisticsRepository(db_session)
        total = await repo.count_total_users(None, None)
        assert total == 2

    @pytest.mark.asyncio
    async def test_count_users_by_role(self, db_session):
        from tests.factories import RoleFactory, UserFactory

        role = await RoleFactory.create(db_session, name="admin")
        await UserFactory.create(db_session, role=role)
        repo = StatisticsRepository(db_session)
        results = await repo.count_users_by_role(None, None)
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_count_total_participations(self, db_session):
        await ParticipationFactory.create(db_session)
        await ParticipationFactory.create(db_session)
        repo = StatisticsRepository(db_session)
        total = await repo.count_total_participations(None, None)
        assert total == 2

    @pytest.mark.asyncio
    async def test_count_participations_by_status(self, db_session):
        await ParticipationFactory.create(db_session, status="registered")
        await ParticipationFactory.create(db_session, status="confirmed")
        repo = StatisticsRepository(db_session)
        results = await repo.count_participations_by_status(None, None)
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_events_per_day(self, db_session):
        await EventFactory.create(db_session)
        await EventFactory.create(db_session)
        repo = StatisticsRepository(db_session)
        results = await repo.events_per_day(None, None)
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_dashboard_overview(self, db_session):
        repo = StatisticsRepository(db_session)
        data = await repo.get_dashboard_overview(None, None)
        assert data is not None
        assert data.total_organizers >= 0
        assert data.total_users >= 0

    @pytest.mark.asyncio
    async def test_time_filtered_query(self, db_session):
        from tests.factories import UserFactory

        await UserFactory.create(db_session)
        repo = StatisticsRepository(db_session)
        dt_from = datetime(2020, 1, 1, tzinfo=UTC)
        dt_to = datetime(2030, 1, 1, tzinfo=UTC)
        total = await repo.count_total_users(dt_from, dt_to)
        assert total == 1
