from typing import Type, Optional, Any

from sqlalchemy import insert, delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.custom_exceptions_http import NotFoundException, NotAddedException, NoUpdateWasMadeException, \
    NoDataWasDeletedException
from infrastructure.db.pg_models.base_model import BaseModel


class BaseRepo:
    def __init__(self, model: Type[BaseModel]):
        self.model: Type[BaseModel] = model

    async def add(self, session: AsyncSession, **kwargs) -> BaseModel:
        query = (
            insert(self.model)
            .values(**kwargs)
            .returning(self.model))
        db_response = await session.execute(query)
        result = db_response.scalar_one_or_none()

        if not result:
            raise NotAddedException(details={
                "model": self.model.__name__,
                "description": "no data was added"
            })
        return result

    async def get(self, session: AsyncSession, **filters) -> Optional[BaseModel]:
        query = select(self.model).filter_by(**filters)
        db_response = await session.execute(query)
        result = db_response.scalar_one_or_none()

        if not result:
            raise NotFoundException(details={
                "model": self.model.__name__,
                "description": "no data was found with exact filters",
                "filters": filters
            })
        return result

    async def get_all(self, session: AsyncSession, **filters) -> list[BaseModel]:
        query = select(self.model).filter_by(**filters)
        db_response = await session.execute(query)
        result = db_response.scalars().all()

        if not result:
            raise NotFoundException(details={
                "model": self.model.__name__,
                "description": "no camera was found"
            })
        return result

    async def update(self, session: AsyncSession, filters: dict[str, Any], values: dict[str, Any]) -> int:
        query = update(self.model).where(
            *[getattr(self.model, k) == v for k, v in filters.items()]
        ).values(**values).execution_options(synchronize_session="fetch")
        db_response = await session.execute(query)
        result = db_response.rowcount
        if not result:
            raise NoUpdateWasMadeException(details={
                "model": self.model.__name__,
                "description": f"no data was updated for {filters}"
            })

        return result

    async def delete(self, session: AsyncSession, **filters) -> int:
        query = delete(self.model).where(
            *[getattr(self.model, k) == v for k, v in filters.items()]
        )
        db_response = await session.execute(query)
        result = db_response.rowcount
        if not result:
            raise NoDataWasDeletedException(details={
                "model": self.model.__name__,
                "description": f"no data was deleted for {filters}"
            })

        return result