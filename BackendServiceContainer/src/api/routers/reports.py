from decimal import Decimal
from fastapi import APIRouter, Depends
from ..core.security import require_role, TokenData
from ..schemas.reports import SummaryReport

router = APIRouter()

@router.get(
    "/summary",
    response_model=SummaryReport,
    summary="Financial summary report (stub)",
    operation_id="summary_report",
    responses={200: {"description": "Summary report (stub)"}},
)
async def summary_report(_: TokenData = Depends(require_role("user"))) -> SummaryReport:
    """
    Return a stubbed financial summary report for the authenticated user.
    This is a placeholder to be implemented with real aggregation logic.
    """
    inflow = Decimal("1000.00")
    outflow = Decimal("400.00")
    return SummaryReport(total_inflow=inflow, total_outflow=outflow, net=inflow - outflow)
