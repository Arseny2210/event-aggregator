"""Background task dispatcher abstraction.

ImportService depends on BackgroundTaskDispatcher (abstract).
Current implementation uses asyncio.create_task.
Future: CeleryBackgroundTaskDispatcher wraps process() in a Celery task.

This separation ensures no business logic changes are needed
when migrating from asyncio background tasks to Celery.
"""

import asyncio
from abc import ABC, abstractmethod
from collections.abc import Coroutine


class BackgroundTaskDispatcher(ABC):
    """Abstract interface for dispatching background work."""

    @abstractmethod
    def dispatch(self, coro: Coroutine[None, None, None]) -> None: ...


class AsyncioBackgroundTaskDispatcher(BackgroundTaskDispatcher):
    """Dispatches background work using asyncio.create_task."""

    def dispatch(self, coro: Coroutine[None, None, None]) -> None:
        asyncio.create_task(coro)
