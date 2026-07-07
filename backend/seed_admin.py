"""Создание администратора."""

import asyncio

from sqlalchemy import select

from app.core.security import hash_password
from app.database.session import async_session_factory
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User

PERMISSIONS = [
    "event:manage",
    "import:create",
    "import:view",
    "notification:send",
    "notification:view",
    "notification:manage",
    "statistics:view",
    "user:view",
    "role:view",
    "permission:view",
    "organizer:manage",
    "organizer:delete",
]


async def seed() -> None:
    async with async_session_factory() as session, session.begin():
        result = await session.execute(
            select(Role).where(Role.name.in_(["administrator", "admin"]))
        )
        roles = result.scalars().all()
        if roles:
            role = roles[0]
            for dup in roles[1:]:
                session.delete(dup)
            if role.name == "admin":
                role.name = "administrator"
                await session.flush()
        else:
            role = Role(name="administrator")
            session.add(role)
            await session.flush()

        for perm_name in PERMISSIONS:
            r = await session.execute(select(Permission).where(Permission.name == perm_name))
            perm = r.scalar_one_or_none()
            if not perm:
                perm = Permission(name=perm_name)
                session.add(perm)
                await session.flush()

            rp = await session.execute(
                select(RolePermission).where(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == perm.id,
                )
            )
            if not rp.scalar_one_or_none():
                session.add(RolePermission(role_id=role.id, permission_id=perm.id))

        r = await session.execute(select(User).where(User.username == "admin"))
        if not r.scalar_one_or_none():
            user = User(
                username="admin",
                email="admin@bgitu.ru",
                password_hash=hash_password("admin123"),
                role_id=role.id,
                is_active=True,
            )
            session.add(user)
            print("Администратор создан: admin / admin123")
        else:
            print("Администратор уже существует")


if __name__ == "__main__":
    asyncio.run(seed())
