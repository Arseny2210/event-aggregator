"""Shared API v1 schemas — generic pagination model."""

from pydantic import BaseModel


class Page[T](BaseModel):
    """Paginated response wrapper."""

    items: list[T]
    total: int
    offset: int
    limit: int
    has_next: bool
