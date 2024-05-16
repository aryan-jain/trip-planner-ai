import logging
import os
from contextlib import asynccontextmanager, contextmanager

from httpx import get
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

DATABASE_URL: str = os.getenv("PG_URI", "")
DATABASE_SYNC_URL: str = os.getenv("PG_SYNC_URI", "")

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)
sync_engine: Engine = create_engine(
    DATABASE_SYNC_URL, echo=False, pool_size=10, max_overflow=0
)


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


@contextmanager
def get_sync_session():
    # The code above is the succint version of the code below
    with Session(sync_engine) as session:
        session.begin()
        try:
            yield session
        except Exception as e:
            logger.error(f"Error: {e}")
            session.rollback()
        else:
            session.commit()
