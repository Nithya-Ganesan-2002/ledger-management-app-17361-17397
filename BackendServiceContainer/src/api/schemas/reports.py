from pydantic import BaseModel, Field
from decimal import Decimal

# PUBLIC_INTERFACE
class SummaryReport(BaseModel):
    """Stub schema for financial summary report."""
    total_inflow: Decimal = Field(..., description="Total inflow amount (stub)")
    total_outflow: Decimal = Field(..., description="Total outflow amount (stub)")
    net: Decimal = Field(..., description="Net flow (inflow - outflow)")
