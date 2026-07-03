"""User repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_id(self, entity_id: UUID) -> User | None:
        statement = select(User).where(User.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[User]:
        statement = select(User).where(User.id.in_(ids)).order_by(User.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_role(self, role_id: int, offset: int, limit: int) -> tuple[list[User], int]:
        statement = (
            select(User)
            .where(User.role_id == role_id)
            .order_by(User.username)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = select(func.count()).select_from(User).where(User.role_id == role_id)
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total

    async def get_active_users(self, offset: int, limit: int) -> tuple[list[User], int]:
        statement = (
            select(User)
            .where(User.is_active.is_(True))
            .order_by(User.username)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = select(func.count()).select_from(User).where(User.is_active.is_(True))
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total
