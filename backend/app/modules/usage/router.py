"""Usage vs plan limits. STARTER STUB. TODO(A4): real counters + 402 when over limit."""

from fastapi import APIRouter, Depends

from app.core.security import ANY_MEMBER, Principal, require_role
from app.modules.usage.schemas import Usage

router = APIRouter(tags=["usage"])


@router.get("/usage", response_model=Usage)
def get_usage(_: Principal = Depends(require_role(*ANY_MEMBER))) -> Usage:
    return Usage(
        period="2026-10",
        plan="trial",
        documents_uploaded=3,
        pages_processed=61,
        monthly_page_limit=200,
        exports=1,
        monthly_export_limit=50,
    )
