from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from typing import AsyncGenerator

from app.core.config import settings

# Create async engine with connection pooling options
engine: AsyncEngine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
)

# Async session maker — explicitly typed so Pyright understands the session type
SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an asynchronous database session.
    Ensures that the session closes correctly once the request resolves.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
