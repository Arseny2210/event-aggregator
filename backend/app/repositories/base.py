"""Base repository with generic CRUD operations.

All repositories inherit from BaseRepository.
No business logic, no transactions, no FastAPI dependencies.
"""

from collections.abc import Sequence
from typing import Any, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

T = TypeVar("T")


class BaseRepository[T]:
    """Generic repository with common CRUD and pagination operations."""

    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, entity_id: UUID | int) -> T | None:
        statement = select(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID | int]) -> list[T]:
        statement = select(self.model).where(self.model.id.in_(ids)).order_by(self.model.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def create_many(self, entities: Sequence[T]) -> list[T]:
        self.session.add_all(entities)
        await self.session.flush()
        return list(entities)

    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.flush()

    async def delete_many(self, entities: Sequence[T]) -> None:
        for entity in entities:
            await self.session.delete(entity)
        await self.session.flush()

    async def get_paginated(
        self,
        offset: int,
        limit: int,
        order_by: ColumnElement[Any] | None = None,
    ) -> tuple[list[T], int]:
        statement = select(self.model)

        if order_by is not None:
            statement = statement.order_by(order_by)
        else:
            statement = statement.order_by(self.model.id)

        statement = statement.offset(offset).limit(limit)

        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = select(func.count()).select_from(self.model)
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def count(self) -> int:
        statement = select(func.count()).select_from(self.model)
        result = await self.session.execute(statement)
        return result.scalar_one()
