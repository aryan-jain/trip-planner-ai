import logging
import os
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)

DATABASE_URL: str = os.getenv("PG_URI", "")

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)


def async_session_generator() -> async_sessionmaker:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
    )


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session

    except Exception as e:
        logger.error(f"Error: {e}")
        await session.rollback()
        raise
    finally:
        await session.close()
