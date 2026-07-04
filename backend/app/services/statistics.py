"""Statistics service — orchestrates StatisticsRepository for dashboard data.

Depends ONLY on StatisticsRepository (no AsyncSession injected).
No FastAPI imports. No app.api.* imports. No SQLAlchemy query construction.

Returns Pydantic response DTOs. Ready for future Redis caching.
"""

from app.repositories.statistics import StatisticsRepository
from app.schemas.organizer import OrganizerResponse
from app.schemas.statistics import (
    ChartDataResponse,
    ChartSeries,
    DashboardOverviewResponse,
    EventStatisticsResponse,
    EventStatusCounts,
    ImportStatisticsResponse,
    ImportStatusCounts,
    OrganizerStatisticsResponse,
    OrganizerSummary,
    ParticipationStatisticsResponse,
    ParticipationStatusCounts,
    RoleUserCountResponse,
    TimeRangeFilter,
    TimeSeriesPoint,
    UserStatisticsResponse,
)


class StatisticsService:
    """Orchestrates read-only statistics queries via StatisticsRepository."""

    def __init__(self, repository: StatisticsRepository) -> None:
        self.repository = repository

    # ---- Private mapping helpers ----

    @staticmethod
    def _map_event_status_counts(counts) -> EventStatusCounts:
        status_map = {c.status: c.count for c in counts}
        return EventStatusCounts(
            draft=status_map.get("draft", 0),
            published=status_map.get("published", 0),
            completed=status_map.get("completed", 0),
            archived=status_map.get("archived", 0),
        )

    @staticmethod
    def _map_organizer_summaries(rows) -> list[OrganizerSummary]:
        return [
            OrganizerSummary(id=r.organizer_id, name=r.organizer_name, event_count=r.event_count)
            for r in rows
        ]

    @staticmethod
    def _map_organizer_responses(organizers) -> list[OrganizerResponse]:
        return [OrganizerResponse.model_validate(o) for o in organizers]

    @staticmethod
    def _map_role_user_counts(rows) -> list[RoleUserCountResponse]:
        return [
            RoleUserCountResponse(role_id=r.role_id, role_name=r.role_name, user_count=r.user_count)
            for r in rows
        ]

    @staticmethod
    def _map_participation_status_counts(counts) -> ParticipationStatusCounts:
        status_map = {c.status: c.count for c in counts}
        return ParticipationStatusCounts(
            registered=status_map.get("registered", 0),
            confirmed=status_map.get("confirmed", 0),
            cancelled=status_map.get("cancelled", 0),
        )

    @staticmethod
    def _map_import_status_counts(counts) -> ImportStatusCounts:
        status_map = {c.status: c.count for c in counts}
        return ImportStatusCounts(
            processing=status_map.get("processing", 0),
            completed=status_map.get("completed", 0),
            failed=status_map.get("failed", 0),
        )

    @staticmethod
    def _sum_event_counts(counts) -> int:
        return sum(c.count for c in counts)

    # ---- Dashboard overview ----

    async def get_dashboard_overview(self, filters: TimeRangeFilter) -> DashboardOverviewResponse:
        dt_from, dt_to = filters.resolve()
        data = await self.repository.get_dashboard_overview(dt_from, dt_to)
        return DashboardOverviewResponse(
            events=EventStatisticsResponse(
                total=self._sum_event_counts(data.event_status_counts),
                by_status=self._map_event_status_counts(data.event_status_counts),
            ),
            organizers=OrganizerStatisticsResponse(
                total=data.total_organizers,
                top_by_events=self._map_organizer_summaries(data.top_organizers),
                newest=self._map_organizer_responses(data.newest_organizers),
            ),
            users=UserStatisticsResponse(
                total=data.total_users,
                by_role=self._map_role_user_counts(data.role_user_counts),
            ),
            participations=ParticipationStatisticsResponse(
                total=data.total_participations,
                by_status=self._map_participation_status_counts(data.participation_status_counts),
                over_time=[
                    TimeSeriesPoint(date=d.day, count=d.count) for d in data.participation_daily
                ],
            ),
            imports=ImportStatisticsResponse(
                total=data.import_aggregates.total_jobs,
                by_status=self._map_import_status_counts(data.import_status_counts),
                total_imported_rows=data.import_aggregates.total_imported_rows,
                total_failed_rows=data.import_aggregates.total_failed_rows,
                average_duration=data.import_aggregates.average_duration,
            ),
        )

    # ---- Event statistics ----

    async def get_event_statistics(self, filters: TimeRangeFilter) -> EventStatisticsResponse:
        dt_from, dt_to = filters.resolve()
        counts = await self.repository.count_events_by_status(dt_from, dt_to)
        return EventStatisticsResponse(
            total=self._sum_event_counts(counts),
            by_status=self._map_event_status_counts(counts),
        )

    # ---- Organizer statistics ----

    async def get_organizer_statistics(
        self, filters: TimeRangeFilter
    ) -> OrganizerStatisticsResponse:
        dt_from, dt_to = filters.resolve()
        total = await self.repository.count_total_organizers(dt_from, dt_to)
        top = await self.repository.top_organizers_by_event_count(5, dt_from, dt_to)
        newest = await self.repository.newest_organizers(5)
        return OrganizerStatisticsResponse(
            total=total,
            top_by_events=self._map_organizer_summaries(top),
            newest=self._map_organizer_responses(newest),
        )

    # ---- User statistics ----

    async def get_user_statistics(self, filters: TimeRangeFilter) -> UserStatisticsResponse:
        dt_from, dt_to = filters.resolve()
        total = await self.repository.count_total_users(dt_from, dt_to)
        role_counts = await self.repository.count_users_by_role(dt_from, dt_to)
        return UserStatisticsResponse(
            total=total,
            by_role=self._map_role_user_counts(role_counts),
        )

    # ---- Participation statistics ----

    async def get_participation_statistics(
        self, filters: TimeRangeFilter
    ) -> ParticipationStatisticsResponse:
        dt_from, dt_to = filters.resolve()
        total = await self.repository.count_total_participations(dt_from, dt_to)
        status_counts = await self.repository.count_participations_by_status(dt_from, dt_to)
        daily = await self.repository.participations_per_day(dt_from, dt_to)
        return ParticipationStatisticsResponse(
            total=total,
            by_status=self._map_participation_status_counts(status_counts),
            over_time=[TimeSeriesPoint(date=d.day, count=d.count) for d in daily],
        )

    # ---- Import statistics ----

    async def get_import_statistics(self, filters: TimeRangeFilter) -> ImportStatisticsResponse:
        dt_from, dt_to = filters.resolve()
        status_counts = await self.repository.count_imports_by_status(dt_from, dt_to)
        aggregates = await self.repository.get_import_aggregates(dt_from, dt_to)
        return ImportStatisticsResponse(
            total=aggregates.total_jobs,
            by_status=self._map_import_status_counts(status_counts),
            total_imported_rows=aggregates.total_imported_rows,
            total_failed_rows=aggregates.total_failed_rows,
            average_duration=aggregates.average_duration,
        )

    # ---- Chart data ----

    async def get_chart_data(self, filters: TimeRangeFilter) -> ChartDataResponse:
        dt_from, dt_to = filters.resolve()
        events_per_day = await self.repository.events_per_day(dt_from, dt_to)
        imports_per_day = await self.repository.imports_per_day(dt_from, dt_to)
        registrations_per_day = await self.repository.participations_per_day(dt_from, dt_to)
        event_status_counts = await self.repository.count_events_by_status(dt_from, dt_to)
        top_by_organizer = await self.repository.events_by_organizer(10, dt_from, dt_to)
        return ChartDataResponse(
            events_per_day=[TimeSeriesPoint(date=d.day, count=d.count) for d in events_per_day],
            imports_per_day=[TimeSeriesPoint(date=d.day, count=d.count) for d in imports_per_day],
            registrations_per_day=[
                TimeSeriesPoint(date=d.day, count=d.count) for d in registrations_per_day
            ],
            events_by_status=[
                ChartSeries(label=c.status.value, value=c.count) for c in event_status_counts
            ],
            events_by_organizer=[
                ChartSeries(label=r.organizer_name, value=r.event_count) for r in top_by_organizer
            ],
        )
