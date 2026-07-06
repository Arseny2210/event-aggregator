"""Category repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Category)

    async def get_all(self) -> list[Category]:
        statement = select(Category).order_by(Category.name)
        result = await self.session.execute(statement)
        return list(result.scalars().all())
