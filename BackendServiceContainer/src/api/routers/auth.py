from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..services.auth_service import authenticate_user, issue_token_for_user
from ..schemas.auth import LoginRequest, AuthToken

router = APIRouter()

@router.post(
    "/login",
    response_model=AuthToken,
    summary="User login",
    operation_id="auth_login",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Unauthorized"},
    },
)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_db)) -> AuthToken:
    """
    Authenticate a user and receive a JWT.

    Parameters:
        payload: LoginRequest containing username and password.
    Returns:
        AuthToken: Bearer token to be used in Authorization header.
    """
    user = await authenticate_user(session, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = await issue_token_for_user(user)
    return AuthToken(token=token)
