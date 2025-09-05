from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_role, TokenData
from ..schemas.transactions import TransactionIn, TransactionOut
from ..services.transaction_service import create_transaction, list_transactions_for_user

router = APIRouter()

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transaction",
    operation_id="create_transaction",
    responses={
        201: {"description": "Transaction created successfully"},
        400: {"description": "Invalid input"},
        401: {"description": "Unauthorized"},
    },
)
async def create_transaction_endpoint(
    payload: TransactionIn,
    session: AsyncSession = Depends(get_db),
    token: TokenData = Depends(require_role("user")),
) -> dict:
    """
    Create a new transaction for the authenticated user.

    Parameters:
        payload: TransactionIn object containing amount, date, category, description.
    Returns:
        Dict with created transaction id.
    """
    created = await create_transaction(session, int(token.sub), payload)
    await session.commit()
    return {"id": created.id}

@router.get(
    "",
    response_model=list[TransactionOut],
    summary="List user's transactions",
    operation_id="list_transactions",
    responses={
        200: {"description": "List of transactions"},
        401: {"description": "Unauthorized"},
    },
)
async def list_my_transactions(
    session: AsyncSession = Depends(get_db),
    token: TokenData = Depends(require_role("user")),
) -> list[TransactionOut]:
    """
    List transactions for the authenticated user.
    """
    items = await list_transactions_for_user(session, int(token.sub))
    return items
