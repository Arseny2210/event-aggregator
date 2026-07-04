"""Domain-level query objects for Event advanced search.

Plain dataclasses and enums — no FastAPI, no Pydantic, no web-framework
imports. Safe for import by the repository layer.
"""

import enum
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.models.enums import EventStatus


class EventSort(enum.Enum):
    DATE_ASC = "date"
    DATE_DESC = "-date"
    TITLE_ASC = "title"
    TITLE_DESC = "-title"
    CREATED_AT_ASC = "created_at"
    CREATED_AT_DESC = "-created_at"
    UPDATED_AT_ASC = "updated_at"
    UPDATED_AT_DESC = "-updated_at"


@dataclass(frozen=True, slots=True)
class EventSearchFilters:
    search: str | None = None
    status: EventStatus | None = None
    organizer_id: UUID | None = None
    organizer_name: str | None = None
    category_id: UUID | None = None
    date_from: date | None = None
    date_to: date | None = None
    sort: EventSort = EventSort.DATE_ASC

    def __post_init__(self) -> None:
        if (
            self.date_from is not None
            and self.date_to is not None
            and self.date_from > self.date_to
        ):
            raise ValueError("date_from must be <= date_to")
