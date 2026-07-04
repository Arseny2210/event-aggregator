"""Factory-boy factories for test data generation."""

from factory.alchemy import SQLAlchemyModelFactory


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory with synchronous session support for factory-boy compatibility."""

    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "flush"
