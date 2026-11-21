from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def create(self, **kwargs) -> T:
        """Создать запись."""
        obj = self.model(**kwargs)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def get_by_id(self, id: UUID) -> T | None:
        """Получить по ID"""
        return await self.session.get(self.model, id)

    async def update(self, id: UUID, **kwargs) -> T | None:
        """Обновить запись."""
        obj = await self.get_by_id(id)

        if obj is None:
            return None

        for key, value in kwargs.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def delete(self, id: UUID) -> bool:
        """Удалить запись."""
        obj = await self.get_by_id(id)

        if obj is None:
            return False

        await self.session.delete(obj)
        await self.session.commit()

        return True

    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[T]:
        """Получить все записи с пагинацией."""
        stmt = select(self.model).limit(limit).offset(offset)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
