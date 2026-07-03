from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.database.session import engine

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")
    await engine.dispose()
