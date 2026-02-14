from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import settings
from app.infra.db.instrumentation import setup_sql_timing

engine = create_async_engine(settings.database_url_async, pool_pre_ping=True)

setup_sql_timing(engine.sync_engine)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
