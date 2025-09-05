import asyncio
from sqlalchemy import select
from ..core.db import Base, _engine, AsyncSessionLocal
from ..models.entities import User
from ..services.auth_service import _hash_password, _salt

async def _create_tables():
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def _seed_users():
    async with AsyncSessionLocal() as session:
        exists = (await session.execute(select(User).where(User.username == "admin"))).scalar_one_or_none()
        if not exists:
            user = User(
                username="admin",
                password_hash=_hash_password("admin", _salt()),
                role="admin",
            )
            session.add(user)
            await session.commit()

# PUBLIC_INTERFACE
def bootstrap_sync() -> None:
    """Create tables and seed minimal data if needed."""
    asyncio.run(_create_tables())
    asyncio.run(_seed_users())
