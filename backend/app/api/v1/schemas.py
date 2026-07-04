"""Shared API DTOs including the Page[T] generic pagination wrapper."""

from pydantic import BaseModel, ConfigDict


class Page[T: BaseModel](BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[T]
    total: int
    offset: int
    limit: int

    @property
    def has_next(self) -> bool:
        return self.offset + self.limit < self.total
