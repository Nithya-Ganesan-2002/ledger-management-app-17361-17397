from datetime import datetime, timedelta, timezone
from typing import Optional, Literal, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel
from .settings import get_settings

settings = get_settings()
bearer_scheme = HTTPBearer(auto_error=False)

class TokenData(BaseModel):
    sub: str
    role: Literal["admin", "user"]
    exp: int

# PUBLIC_INTERFACE
def create_access_token(subject: str, role: Literal["admin", "user"], expires_minutes: Optional[int] = None) -> str:
    """Create a JWT access token."""
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes or settings.JWT_EXPIRES_MINUTES)
    payload = {"sub": subject, "role": role, "exp": int(expire.timestamp())}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

# PUBLIC_INTERFACE
def decode_access_token(token: str) -> TokenData:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# PUBLIC_INTERFACE
async def get_current_token(creds: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)]) -> TokenData:
    """FastAPI dependency to get and verify the current token."""
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return decode_access_token(creds.credentials)

# PUBLIC_INTERFACE
def require_role(required: Literal["admin", "user"]):
    """Return a dependency that checks the user's role."""
    async def _enforce_role(token: Annotated[TokenData, Depends(get_current_token)]) -> TokenData:
        allowed = token.role == "admin" or token.role == required
        if not allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return token
    return _enforce_role
