from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.entities import Transaction
from ..schemas.transactions import TransactionIn, TransactionOut

# PUBLIC_INTERFACE
async def create_transaction(session: AsyncSession, user_id: int, data: TransactionIn) -> TransactionOut:
    """Create a new transaction for a user."""
    tx = Transaction(
        amount=data.amount,
        date=data.date,
        category=data.category,
        description=data.description,
        user_id=user_id,
    )
    session.add(tx)
    await session.flush()  # obtain PK
    await session.refresh(tx)
    return TransactionOut(
        id=tx.id,
        amount=tx.amount,
        date=tx.date,
        category=tx.category,
        description=tx.description,
        user_id=tx.user_id,
    )

# PUBLIC_INTERFACE
async def list_transactions_for_user(session: AsyncSession, user_id: int) -> list[TransactionOut]:
    """List transactions belonging to a user."""
    result = await session.execute(select(Transaction).where(Transaction.user_id == user_id))
    items = result.scalars().all()
    return [
        TransactionOut(
            id=tx.id,
            amount=tx.amount,
            date=tx.date,
            category=tx.category,
            description=tx.description,
            user_id=tx.user_id,
        )
        for tx in items
    ]
