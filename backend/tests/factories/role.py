"""Role and permission factories."""

import factory
from faker import Faker

from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from tests.factories.base import BaseFactory

faker = Faker()


class PermissionFactory(BaseFactory):
    class Meta:
        model = Permission

    name = factory.Sequence(lambda n: f"test_permission_{n}")
    description = factory.LazyFunction(lambda: faker.sentence())


class RoleFactory(BaseFactory):
    class Meta:
        model = Role

    name = factory.Sequence(lambda n: f"test_role_{n}")
    description = factory.LazyFunction(lambda: faker.sentence())


class RolePermissionFactory(BaseFactory):
    class Meta:
        model = RolePermission

    role = factory.SubFactory(RoleFactory)
    permission = factory.SubFactory(PermissionFactory)
