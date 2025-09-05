import os
import hmac
import hashlib
from typing import Optional, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.entities import User
from ..core.security import create_access_token

def _hash_password(password: str, salt: bytes) -> str:
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return dk.hex()

def _salt() -> bytes:
    # In production, use a per-user random salt stored with the hash.
    # For simplicity, we derive a consistent salt from env (better than hardcoding).
    env_salt = os.getenv("PASSWORD_SALT", "set-a-strong-salt-in-env").encode("utf-8")
    return hashlib.sha256(env_salt).digest()

# PUBLIC_INTERFACE
async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
    """Authenticate a user by username and password."""
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        return None
    expected = user.password_hash
    candidate = _hash_password(password, _salt())
    if not hmac.compare_digest(expected, candidate):
        return None
    return user

# PUBLIC_INTERFACE
async def issue_token_for_user(user: User) -> str:
    """Create JWT for the given user."""
    role: Literal["admin", "user"] = "admin" if user.role == "admin" else "user"
    return create_access_token(subject=str(user.id), role=role)
