"""Statistics and dashboard DTOs.

Framework-free query objects (frozen dataclasses) and Pydantic response
schemas. No FastAPI, no app.api imports — safe for repository and service
layer use.
"""

import enum
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseSchema


class TimeRange(enum.Enum):
    TODAY = "today"
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    CURRENT_MONTH = "current_month"
    CUSTOM = "custom"


@dataclass(frozen=True, slots=True)
class TimeRangeFilter:
    period: TimeRange | None = None
    date_from: date | None = None
    date_to: date | None = None

    def __post_init__(self) -> None:
        if self.period == TimeRange.CUSTOM:
            if self.date_from is None or self.date_to is None:
                raise ValueError("CUSTOM period requires both date_from and date_to")
            if self.date_from > self.date_to:
                raise ValueError("date_from must be <= date_to")

    def resolve(self) -> tuple[datetime | None, datetime | None]:
        if self.period is None:
            return None, None
        today = date.today()
        match self.period:
            case TimeRange.TODAY:
                start = datetime.combine(today, time.min, tzinfo=UTC)
                end = datetime.combine(today, time.max, tzinfo=UTC)
            case TimeRange.LAST_7_DAYS:
                start = datetime.combine(today - timedelta(days=7), time.min, tzinfo=UTC)
                end = datetime.combine(today, time.max, tzinfo=UTC)
            case TimeRange.LAST_30_DAYS:
                start = datetime.combine(today - timedelta(days=30), time.min, tzinfo=UTC)
                end = datetime.combine(today, time.max, tzinfo=UTC)
            case TimeRange.CURRENT_MONTH:
                first = today.replace(day=1)
                start = datetime.combine(first, time.min, tzinfo=UTC)
                end = datetime.combine(today, time.max, tzinfo=UTC)
            case TimeRange.CUSTOM:
                start = datetime.combine(
                    self.date_from,
                    time.min,
                    tzinfo=UTC,  # type: ignore[arg-type]
                )
                end = datetime.combine(
                    self.date_to,
                    time.max,
                    tzinfo=UTC,  # type: ignore[arg-type]
                )
        return start, end


# ---- Pydantic response DTOs ----


class EventStatusCounts(BaseSchema):
    draft: int = Field(default=0, ge=0)
    published: int = Field(default=0, ge=0)
    completed: int = Field(default=0, ge=0)
    archived: int = Field(default=0, ge=0)


class EventStatisticsResponse(BaseSchema):
    total: int
    by_status: EventStatusCounts


class OrganizerSummary(BaseSchema):
    id: UUID
    name: str
    event_count: int


class OrganizerStatisticsResponse(BaseSchema):
    total: int
    top_by_events: list[OrganizerSummary]
    newest: list["OrganizerResponse"]


class RoleUserCountResponse(BaseSchema):
    role_id: int
    role_name: str
    user_count: int


class UserStatisticsResponse(BaseSchema):
    total: int
    by_role: list[RoleUserCountResponse]


class ParticipationStatusCounts(BaseSchema):
    registered: int = Field(default=0, ge=0)
    confirmed: int = Field(default=0, ge=0)
    cancelled: int = Field(default=0, ge=0)


class TimeSeriesPoint(BaseSchema):
    date: date
    count: int


class ParticipationStatisticsResponse(BaseSchema):
    total: int
    by_status: ParticipationStatusCounts
    over_time: list[TimeSeriesPoint]


class ImportStatusCounts(BaseSchema):
    processing: int = Field(default=0, ge=0)
    completed: int = Field(default=0, ge=0)
    failed: int = Field(default=0, ge=0)


class ImportStatisticsResponse(BaseSchema):
    total: int
    by_status: ImportStatusCounts
    total_imported_rows: int
    total_failed_rows: int
    average_duration: float | None


class ChartSeries(BaseSchema):
    label: str
    value: int


class ChartDataResponse(BaseSchema):
    events_per_day: list[TimeSeriesPoint]
    imports_per_day: list[TimeSeriesPoint]
    registrations_per_day: list[TimeSeriesPoint]
    events_by_status: list[ChartSeries]
    events_by_organizer: list[ChartSeries]


class DashboardOverviewResponse(BaseSchema):
    events: EventStatisticsResponse
    organizers: OrganizerStatisticsResponse
    users: UserStatisticsResponse
    participations: ParticipationStatisticsResponse
    imports: ImportStatisticsResponse


from app.schemas.organizer import OrganizerResponse  # noqa: E402  (resolve forward ref)
