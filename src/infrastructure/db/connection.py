from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

engine = create_async_engine(settings.get_url_pg)

AsyncSessionMaker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)