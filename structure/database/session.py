from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .base import Base
from .config import get_database_url

ENGINE = create_async_engine(get_database_url(), pool_pre_ping=True)
ASYNC_SESSION_FACTORY = async_sessionmaker(ENGINE, expire_on_commit=False)
async_session = ASYNC_SESSION_FACTORY


async def get_session() -> AsyncIterator[AsyncSession]:
    """Возвращаем async сессию."""

    async with ASYNC_SESSION_FACTORY() as session:
        yield session


async def init_models() -> None:
    """Создаём таблицы если их ещё нет."""

    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


__all__ = [
    "ENGINE",
    "ASYNC_SESSION_FACTORY",
    "async_session",
    "get_session",
    "init_models",
]
