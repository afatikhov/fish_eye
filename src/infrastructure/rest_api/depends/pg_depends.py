from infrastructure.db.connection import AsyncSessionMaker


async def get_pg_db():
    async with AsyncSessionMaker() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise