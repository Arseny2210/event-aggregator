"""Generic base repository for SQLAlchemy 2.0 Async."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ColumnExpressionArgument


class BaseRepository[T]:
    """Generic async repository with CRUD, pagination, and batch operations."""

    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

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

    async def count(self) -> int:
        statement = select(func.count()).select_from(self.model)
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def get_paginated(
        self,
        offset: int,
        limit: int,
        order_by: ColumnExpressionArgument[Any] | None = None,
    ) -> tuple[list[T], int]:
        count_stmt = select(func.count()).select_from(self.model)
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = select(self.model).offset(offset).limit(limit)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())
        return items, total
