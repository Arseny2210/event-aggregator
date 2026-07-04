from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import engine

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await conn.commit()
        logger.info("Database connection verified")
    except Exception as exc:
        logger.warning("Database connection check failed: %s", exc)
    yield
    logger.info("Application shutdown")
    await engine.dispose()
