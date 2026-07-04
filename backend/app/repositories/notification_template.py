"""NotificationTemplate repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import NotificationChannelType, NotificationTemplateType
from app.models.notification_template import NotificationTemplate
from app.repositories.base import BaseRepository


class NotificationTemplateRepository(BaseRepository[NotificationTemplate]):
    """Repository for NotificationTemplate entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, NotificationTemplate)

    async def get_by_id(self, entity_id: UUID) -> NotificationTemplate | None:
        statement = select(NotificationTemplate).where(NotificationTemplate.id == entity_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi_by_ids(self, ids: Sequence[UUID]) -> list[NotificationTemplate]:
        statement = (
            select(NotificationTemplate)
            .where(NotificationTemplate.id.in_(ids))
            .order_by(NotificationTemplate.id)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_type_channel_language(
        self,
        template_type: NotificationTemplateType,
        channel: NotificationChannelType,
        language: str = "en",
        version: int | None = None,
    ) -> NotificationTemplate | None:
        statement = select(NotificationTemplate).where(
            NotificationTemplate.template_type == template_type,
            NotificationTemplate.channel == channel,
            NotificationTemplate.language == language,
            NotificationTemplate.is_active.is_(True),
        )
        if version is not None:
            statement = statement.where(NotificationTemplate.version == version)
        else:
            statement = statement.order_by(NotificationTemplate.version.desc()).limit(1)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all_active(
        self, offset: int, limit: int
    ) -> tuple[list[NotificationTemplate], int]:
        statement = (
            select(NotificationTemplate)
            .where(NotificationTemplate.is_active.is_(True))
            .order_by(NotificationTemplate.template_type, NotificationTemplate.channel)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        items = list(result.scalars().all())

        count_statement = (
            select(func.count())
            .select_from(NotificationTemplate)
            .where(NotificationTemplate.is_active.is_(True))
        )
        count_result = await self.session.execute(count_statement)
        total = count_result.scalar_one()

        return items, total
