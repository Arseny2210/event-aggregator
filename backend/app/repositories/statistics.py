"""Statistics repository — read-only SQLAlchemy aggregate queries.

No FastAPI imports. No HTTP concepts. No business logic.
Returns frozen dataclass row types only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import EventStatus, ImportStatus, ParticipationStatus
from app.models.event import Event
from app.models.import_job import ImportJob
from app.models.organizer import Organizer
from app.models.participation import Participation
from app.models.role import Role
from app.models.user import User


@dataclass(frozen=True, slots=True)
class EventStatusCount:
    status: EventStatus
    count: int


@dataclass(frozen=True, slots=True)
class OrganizerEventCount:
    organizer_id: UUID
    organizer_name: str
    event_count: int


@dataclass(frozen=True, slots=True)
class RoleUserCountRow:
    role_id: int
    role_name: str
    user_count: int


@dataclass(frozen=True, slots=True)
class ParticipationStatusCount:
    status: ParticipationStatus
    count: int


@dataclass(frozen=True, slots=True)
class ImportStatusCount:
    status: ImportStatus
    count: int


@dataclass(frozen=True, slots=True)
class DailyCount:
    day: date
    count: int


@dataclass(frozen=True, slots=True)
class ImportAggregate:
    total_jobs: int
    total_imported_rows: int
    total_failed_rows: int
    average_duration: float | None


@dataclass(frozen=True, slots=True)
class DashboardOverviewData:
    event_status_counts: list[EventStatusCount]
    total_organizers: int
    top_organizers: list[OrganizerEventCount]
    newest_organizers: list[Organizer]
    total_users: int
    role_user_counts: list[RoleUserCountRow]
    total_participations: int
    participation_status_counts: list[ParticipationStatusCount]
    participation_daily: list[DailyCount]
    import_status_counts: list[ImportStatusCount]
    import_aggregates: ImportAggregate


def _apply_created_at_filter(
    stmt, model, datetime_from: datetime | None, datetime_to: datetime | None
):
    if datetime_from is not None:
        stmt = stmt.where(model.created_at >= datetime_from)
    if datetime_to is not None:
        stmt = stmt.where(model.created_at <= datetime_to)
    return stmt


class StatisticsRepository:
    """Read-only repository for aggregated statistics across multiple models."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ---- Dashboard overview (adjustment #3: single method) ----

    async def get_dashboard_overview(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> DashboardOverviewData:
        event_status_counts = await self.count_events_by_status(datetime_from, datetime_to)
        total_organizers = await self.count_total_organizers(datetime_from, datetime_to)
        top_organizers = await self.top_organizers_by_event_count(5, datetime_from, datetime_to)
        newest_organizers = await self.newest_organizers(5)
        total_users = await self.count_total_users(datetime_from, datetime_to)
        role_user_counts = await self.count_users_by_role(datetime_from, datetime_to)
        total_participations = await self.count_total_participations(datetime_from, datetime_to)
        participation_status_counts = await self.count_participations_by_status(
            datetime_from, datetime_to
        )
        participation_daily = await self.participations_per_day(datetime_from, datetime_to)
        import_status_counts = await self.count_imports_by_status(datetime_from, datetime_to)
        import_aggregates = await self.get_import_aggregates(datetime_from, datetime_to)
        return DashboardOverviewData(
            event_status_counts=event_status_counts,
            total_organizers=total_organizers,
            top_organizers=top_organizers,
            newest_organizers=newest_organizers,
            total_users=total_users,
            role_user_counts=role_user_counts,
            total_participations=total_participations,
            participation_status_counts=participation_status_counts,
            participation_daily=participation_daily,
            import_status_counts=import_status_counts,
            import_aggregates=import_aggregates,
        )

    # ---- Events ----

    async def count_events_by_status(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> list[EventStatusCount]:
        stmt = select(Event.status.label("status"), func.count().label("count")).group_by(
            Event.status
        )
        stmt = _apply_created_at_filter(stmt, Event, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [EventStatusCount(status=row.status, count=row.count) for row in result.all()]

    # ---- Organizers ----

    async def count_total_organizers(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> int:
        stmt = select(func.count()).select_from(Organizer)
        stmt = _apply_created_at_filter(stmt, Organizer, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def top_organizers_by_event_count(
        self,
        limit: int,
        datetime_from: datetime | None,
        datetime_to: datetime | None,
    ) -> list[OrganizerEventCount]:
        stmt = (
            select(
                Organizer.id.label("organizer_id"),
                Organizer.name.label("organizer_name"),
                func.count(Event.id).label("event_count"),
            )
            .join(Event, Event.organizer_id == Organizer.id)
            .group_by(Organizer.id, Organizer.name)
            .order_by(func.count(Event.id).desc())
            .limit(limit)
        )
        stmt = _apply_created_at_filter(stmt, Event, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [
            OrganizerEventCount(
                organizer_id=row.organizer_id,
                organizer_name=row.organizer_name,
                event_count=row.event_count,
            )
            for row in result.all()
        ]

    async def newest_organizers(self, limit: int) -> list[Organizer]:
        stmt = select(Organizer).order_by(Organizer.created_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ---- Users ----

    async def count_total_users(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> int:
        stmt = select(func.count()).select_from(User)
        stmt = _apply_created_at_filter(stmt, User, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def count_users_by_role(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> list[RoleUserCountRow]:
        stmt = (
            select(
                Role.id.label("role_id"),
                Role.name.label("role_name"),
                func.count(User.id).label("user_count"),
            )
            .join(User, User.role_id == Role.id)
            .group_by(Role.id, Role.name)
        )
        stmt = _apply_created_at_filter(stmt, User, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [
            RoleUserCountRow(
                role_id=row.role_id,
                role_name=row.role_name,
                user_count=row.user_count,
            )
            for row in result.all()
        ]

    # ---- Participations ----

    async def count_total_participations(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> int:
        stmt = select(func.count()).select_from(Participation)
        stmt = _apply_created_at_filter(stmt, Participation, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def count_participations_by_status(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> list[ParticipationStatusCount]:
        stmt = select(
            Participation.status.label("status"),
            func.count().label("count"),
        ).group_by(Participation.status)
        stmt = _apply_created_at_filter(stmt, Participation, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [
            ParticipationStatusCount(status=row.status, count=row.count) for row in result.all()
        ]

    async def participations_per_day(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> list[DailyCount]:
        stmt = (
            select(
                cast(Participation.created_at, Date).label("day"),
                func.count().label("count"),
            )
            .group_by(cast(Participation.created_at, Date))
            .order_by("day")
        )
        stmt = _apply_created_at_filter(stmt, Participation, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [DailyCount(day=row.day, count=row.count) for row in result.all()]

    # ---- Imports ----

    async def count_imports_by_status(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> list[ImportStatusCount]:
        stmt = select(
            ImportJob.status.label("status"),
            func.count().label("count"),
        ).group_by(ImportJob.status)
        stmt = _apply_created_at_filter(stmt, ImportJob, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [ImportStatusCount(status=row.status, count=row.count) for row in result.all()]

    async def get_import_aggregates(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> ImportAggregate:
        stmt = select(
            func.count().label("total_jobs"),
            func.coalesce(func.sum(ImportJob.imported_rows), 0).label("total_imported_rows"),
            func.coalesce(func.sum(ImportJob.failed_rows), 0).label("total_failed_rows"),
            func.avg(ImportJob.duration).label("average_duration"),
        )
        stmt = _apply_created_at_filter(stmt, ImportJob, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        row = result.one()
        return ImportAggregate(
            total_jobs=row.total_jobs,
            total_imported_rows=row.total_imported_rows,
            total_failed_rows=row.total_failed_rows,
            average_duration=(
                float(row.average_duration) if row.average_duration is not None else None
            ),
        )

    # ---- Charts ----

    async def events_per_day(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> list[DailyCount]:
        stmt = (
            select(
                cast(Event.created_at, Date).label("day"),
                func.count().label("count"),
            )
            .group_by(cast(Event.created_at, Date))
            .order_by("day")
        )
        stmt = _apply_created_at_filter(stmt, Event, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [DailyCount(day=row.day, count=row.count) for row in result.all()]

    async def imports_per_day(
        self, datetime_from: datetime | None, datetime_to: datetime | None
    ) -> list[DailyCount]:
        stmt = (
            select(
                cast(ImportJob.created_at, Date).label("day"),
                func.count().label("count"),
            )
            .group_by(cast(ImportJob.created_at, Date))
            .order_by("day")
        )
        stmt = _apply_created_at_filter(stmt, ImportJob, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [DailyCount(day=row.day, count=row.count) for row in result.all()]

    async def events_by_organizer(
        self,
        limit: int,
        datetime_from: datetime | None,
        datetime_to: datetime | None,
    ) -> list[OrganizerEventCount]:
        stmt = (
            select(
                Organizer.id.label("organizer_id"),
                Organizer.name.label("organizer_name"),
                func.count(Event.id).label("event_count"),
            )
            .join(Event, Event.organizer_id == Organizer.id)
            .group_by(Organizer.id, Organizer.name)
            .order_by(func.count(Event.id).desc())
            .limit(limit)
        )
        stmt = _apply_created_at_filter(stmt, Event, datetime_from, datetime_to)
        result = await self.session.execute(stmt)
        return [
            OrganizerEventCount(
                organizer_id=row.organizer_id,
                organizer_name=row.organizer_name,
                event_count=row.event_count,
            )
            for row in result.all()
        ]
