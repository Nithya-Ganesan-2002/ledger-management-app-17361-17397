from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional

# PUBLIC_INTERFACE
class TransactionIn(BaseModel):
    """Incoming transaction payload as per OpenAPI."""
    amount: Decimal = Field(..., description="Transaction amount")
    date: datetime = Field(..., description="Transaction date-time (ISO8601)")
    category: str = Field(..., description="Transaction category label")
    description: Optional[str] = Field(None, description="Optional description")

# PUBLIC_INTERFACE
class TransactionOut(TransactionIn):
    """Transaction returned to clients."""
    id: int = Field(..., description="Transaction unique identifier")
    user_id: int = Field(..., description="ID of the user who created the transaction")
