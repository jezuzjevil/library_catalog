from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from library_catalog.core.config import get_settings

settings = get_settings()


# Базовый класс для ORM-моделей
class Base(DeclarativeBase):
    pass


# Асинхронный движок базы данных
engine = create_async_engine(
    str(settings.database_url),
    pool_size=settings.database_pool_size,
    echo=settings.debug,
    pool_pre_ping=True,
)


# Фабрика асинхронных сессий
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency для FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# Проверка доступности базы данных
async def check_db_connection() -> bool:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False


# Инициализация подключения к базе данных
async def init_db() -> None:
    if not await check_db_connection():
        raise RuntimeError("Не удалось подключиться к PostgreSQL")


# Закрытие пула соединений
async def dispose_engine() -> None:
    await engine.dispose()
