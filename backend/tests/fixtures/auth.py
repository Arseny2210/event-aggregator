"""Authentication test fixtures."""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.security import create_access_token
from app.dependencies.database import get_db
from app.main import create_app
from tests.factories import (
    PermissionFactory,
    RoleFactory,
    RolePermissionFactory,
    UserFactory,
)

PERM_LIST = [
    "event:manage",
    "import:create",
    "import:view",
    "notification:send",
    "notification:view",
    "notification:manage",
    "statistics:view",
]


@pytest_asyncio.fixture
async def simple_role(db_session):
    return await RoleFactory.create(db_session, name="test_role")


@pytest_asyncio.fixture
async def simple_user(db_session, simple_role):
    return await UserFactory.create(db_session, role=simple_role)


@pytest_asyncio.fixture
async def admin_role(db_session):
    role = await RoleFactory.create(db_session, name="admin")
    for perm_name in PERM_LIST:
        perm = await PermissionFactory.create(db_session, name=perm_name)
        await RolePermissionFactory.create(db_session, role=role, permission=perm)
    return role


@pytest_asyncio.fixture
async def admin_user(db_session, admin_role):
    return await UserFactory.create(
        db_session,
        username="admin",
        email="admin@test.com",
        role=admin_role,
    )


@pytest_asyncio.fixture
def auth_headers(admin_user):
    token = create_access_token(user_id=admin_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_client(db_session, admin_user):
    """Client authenticated as admin, using the test db_session."""
    app = create_app()

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    token = create_access_token(user_id=admin_user.id)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
    ) as client:
        yield client
