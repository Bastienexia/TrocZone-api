from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from troczone_api.core.config import settings

sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.replace("asyncpg", "psycopg2"),
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=4,
    max_overflow=2,
)

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recyle=300,
    pool_size=4,
    max_overflow=2,
)

SyncSession = sessionmaker(sync_engine)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()
