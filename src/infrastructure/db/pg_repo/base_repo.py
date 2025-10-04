from typing import Type, Optional, Any

from sqlalchemy import insert, delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.pg_models.base_model import BaseModel


class BaseRepo:
    def __init__(self, model: Type[BaseModel]):
        self.model: Type[BaseModel] = model

    async def add(self, session: AsyncSession, **kwargs) -> BaseModel:
        query = (
            insert(self.model)
            .values(**kwargs)
            .returning(self.model))
        res = await session.execute(query)
        return res.scalar_one_or_none()

    async def get(self, session: AsyncSession, **filters) -> Optional[BaseModel]:
        query = select(self.model).filter_by(**filters)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    async def get_all(self, session: AsyncSession, **filters) -> list[BaseModel]:
        query = select(self.model).filter_by(**filters)
        res = await session.execute(query)
        return res.scalars().all()

    async def update(self, session: AsyncSession, filters: dict[str, Any], values: dict[str, Any]) -> int:
        query = update(self.model).where(
            *[getattr(self.model, k) == v for k, v in filters.items()]
        ).values(**values).execution_options(synchronize_session="fetch")
        res = await session.execute(query)
        await session.commit()
        return res.rowcount

    async def delete(self, session: AsyncSession, **filters) -> int:
        query = delete(self.model).where(
            *[getattr(self.model, k) == v for k, v in filters.items()]
        )
        res = await session.execute(query)
        await session.commit()
        return res.rowcount