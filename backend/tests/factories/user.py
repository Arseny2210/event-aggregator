"""User factories."""

import factory
from faker import Faker

from app.core.security import hash_password
from app.models.user import User
from tests.factories.base import BaseFactory
from tests.factories.role import RoleFactory

faker = Faker()


class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.com")
    password_hash = factory.LazyFunction(lambda: hash_password("testpass123"))
    role = factory.SubFactory(RoleFactory)
    is_active = True


class AdminFactory(UserFactory):
    username = factory.Sequence(lambda n: f"admin_{n}")
    role = factory.SubFactory(RoleFactory, name="admin")


class EditorFactory(UserFactory):
    username = factory.Sequence(lambda n: f"editor_{n}")
    role = factory.SubFactory(RoleFactory, name="editor")
