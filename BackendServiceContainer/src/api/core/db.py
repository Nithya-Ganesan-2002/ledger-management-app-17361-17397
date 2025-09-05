from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from .settings import get_settings

Base = declarative_base()

_settings = get_settings()
_engine = create_async_engine(_settings.DB_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(bind=_engine, expire_on_commit=False, class_=AsyncSession)

# PUBLIC_INTERFACE
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async SQLAlchemy session for request scope."""
    async with AsyncSessionLocal() as session:
        yield session
