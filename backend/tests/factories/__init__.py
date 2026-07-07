"""Async test factories using the AsyncSession directly."""

from faker import Faker

from app.core.security import hash_password
from app.models.category import Category
from app.models.enums import (
    EventStatus,
    ImportRowStatus,
    ImportStatus,
    NotificationChannelType,
    NotificationPriority,
    NotificationStatus,
    NotificationTemplateType,
    ParticipationStatus,
)
from app.models.event import Event
from app.models.import_job import ImportJob
from app.models.import_row_result import ImportJobRowResult
from app.models.notification import Notification
from app.models.notification_template import NotificationTemplate
from app.models.organizer import Organizer
from app.models.participation import Participation
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User

faker = Faker()


class RoleFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> Role:
        defaults = {
            "name": kwargs.pop("name", f"role_{faker.unique.word()}"),
            "description": kwargs.pop("description", faker.sentence()),
        }
        defaults.update(kwargs)
        obj = Role(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class PermissionFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> Permission:
        defaults = {
            "name": kwargs.pop("name", f"perm_{faker.unique.word()}"),
            "description": kwargs.pop("description", faker.sentence()),
        }
        defaults.update(kwargs)
        obj = Permission(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class RolePermissionFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> RolePermission:
        if "role" not in kwargs and "role_id" not in kwargs:
            kwargs["role"] = RoleFactory.create(session)
        if "permission" not in kwargs and "permission_id" not in kwargs:
            kwargs["permission"] = PermissionFactory.create(session)
        obj = RolePermission(**kwargs)
        session.add(obj)
        await session.flush()
        return obj


class UserFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> User:
        if "role" not in kwargs and "role_id" not in kwargs:
            role = await RoleFactory.create(session)
            kwargs["role"] = role
        password = kwargs.pop("password", "testpass123")
        defaults = {
            "username": kwargs.pop("username", f"user_{faker.unique.word()}"),
            "email": kwargs.pop("email", f"{faker.unique.word()}@test.com"),
            "password_hash": hash_password(password),
            "is_active": kwargs.pop("is_active", True),
        }
        defaults.update(kwargs)
        obj = User(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class OrganizerFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> Organizer:
        defaults = {"name": kwargs.pop("name", f"organizer_{faker.unique.word()}")}
        defaults.update(kwargs)
        obj = Organizer(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class CategoryFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> Category:
        defaults = {
            "name": kwargs.pop("name", f"category_{faker.unique.word()}"),
        }
        defaults.update(kwargs)
        obj = Category(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class EventFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> Event:
        if "organizer" not in kwargs and "organizer_id" not in kwargs:
            org = await OrganizerFactory.create(session)
            kwargs["organizer"] = org
        if "category" not in kwargs and "category_id" not in kwargs:
            cat = await CategoryFactory.create(session)
            kwargs["category"] = cat
        from datetime import date

        defaults = {
            "title": kwargs.pop("title", faker.sentence(nb_words=4)),
            "description": kwargs.pop("description", faker.paragraph()),
            "status": kwargs.pop("status", EventStatus.draft),
            "start_date": kwargs.pop("start_date", date.today()),
            "location": kwargs.pop("location", faker.city()),
        }
        defaults.update(kwargs)
        obj = Event(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class ParticipationFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> Participation:
        if "event" not in kwargs and "event_id" not in kwargs:
            event = await EventFactory.create(session)
            kwargs["event"] = event
        defaults = {
            "session_id": kwargs.pop("session_id", faker.unique.word()),
            "status": kwargs.pop("status", ParticipationStatus.registered),
        }
        defaults.update(kwargs)
        obj = Participation(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class ImportJobFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> ImportJob:
        if "created_by" not in kwargs:
            user = await UserFactory.create(session)
            kwargs["created_by"] = user.id
        defaults = {
            "filename": kwargs.pop("filename", f"test_{faker.unique.word()}.xlsx"),
            "status": kwargs.pop("status", ImportStatus.processing),
        }
        defaults.update(kwargs)
        obj = ImportJob(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class ImportJobRowResultFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> ImportJobRowResult:
        if "import_job" not in kwargs and "import_job_id" not in kwargs:
            job = await ImportJobFactory.create(session)
            kwargs["import_job"] = job
        defaults = {
            "row_number": kwargs.pop("row_number", faker.random_int(min=1, max=1000)),
            "status": kwargs.pop("status", ImportRowStatus.imported),
        }
        defaults.update(kwargs)
        obj = ImportJobRowResult(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class NotificationTemplateFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> NotificationTemplate:
        defaults = {
            "template_type": kwargs.pop("template_type", NotificationTemplateType.welcome),
            "channel": kwargs.pop("channel", NotificationChannelType.email),
            "subject": kwargs.pop("subject", "Hello {user_name}"),
            "body": kwargs.pop("body", "<p>Welcome, {user_name}!</p>"),
            "language": kwargs.pop("language", "en"),
            "version": kwargs.pop("version", 1),
            "is_active": kwargs.pop("is_active", True),
        }
        defaults.update(kwargs)
        obj = NotificationTemplate(**defaults)
        session.add(obj)
        await session.flush()
        return obj


class NotificationFactory:
    @classmethod
    async def create(cls, session, **kwargs) -> Notification:
        defaults = {
            "channel": kwargs.pop("channel", NotificationChannelType.email),
            "recipient": kwargs.pop("recipient", faker.email()),
            "template_type": kwargs.pop("template_type", NotificationTemplateType.welcome),
            "payload": kwargs.pop("payload", {"test": "data"}),
            "status": kwargs.pop("status", NotificationStatus.pending),
            "priority": kwargs.pop("priority", NotificationPriority.NORMAL),
        }
        defaults.update(kwargs)
        obj = Notification(**defaults)
        session.add(obj)
        await session.flush()
        return obj
