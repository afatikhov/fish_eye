from typing import Type

from sqlalchemy import insert
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