"""Tests for StatisticsService."""

import pytest

from app.repositories.statistics import StatisticsRepository
from app.schemas.statistics import TimeRangeFilter
from app.services.statistics import StatisticsService
from tests.factories import EventFactory


class TestStatisticsService:
    @pytest.mark.asyncio
    async def test_get_event_statistics(self, db_session):
        await EventFactory.create(db_session)
        svc = StatisticsService(repository=StatisticsRepository(db_session))
        result = await svc.get_event_statistics(TimeRangeFilter())
        assert result.total >= 1

    @pytest.mark.asyncio
    async def test_get_chart_data(self, db_session):
        await EventFactory.create(db_session)
        svc = StatisticsService(repository=StatisticsRepository(db_session))
        result = await svc.get_chart_data(TimeRangeFilter())
        assert result is not None
        assert len(result.events_per_day) >= 1

    @pytest.mark.asyncio
    async def test_get_dashboard_overview(self, db_session):
        svc = StatisticsService(repository=StatisticsRepository(db_session))
        result = await svc.get_dashboard_overview(TimeRangeFilter())
        assert result is not None
        assert result.events.total >= 0

    @pytest.mark.asyncio
    async def test_with_time_filter(self, db_session):
        from datetime import date

        await EventFactory.create(db_session)
        svc = StatisticsService(repository=StatisticsRepository(db_session))
        f = TimeRangeFilter(
            period=None,
            date_from=date(2020, 1, 1),
            date_to=date(2030, 1, 1),
        )
        result = await svc.get_event_statistics(f)
        assert result.total >= 1
