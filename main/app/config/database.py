import logging

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.settings import settings


logger = logging.getLogger(settings.LOGGER_NAME)

Base = declarative_base()

async_engine = create_async_engine(settings.DB_URL, future=True, echo=True)
async_local_session = sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_async_session():
    session: AsyncSession = async_local_session()
    try:
        yield session
    except Exception as e:
        logger.error(f"Exception from get_async_session - {e}")
        await session.rollback()
    finally:
        await session.close()


def async_session(func):
    async def _wrapper(*args, **kwargs):
        async with get_async_session() as session:
            return await func(*args, session, **kwargs)

    return _wrapper
