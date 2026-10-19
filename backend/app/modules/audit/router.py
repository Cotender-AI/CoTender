"""Audit trail. STARTER STUB. TODO(A4): real implementation (admin only)."""

from fastapi import APIRouter, Depends

from app.core import examples as ex
from app.core.models.enums import Role
from app.core.schemas import Page
from app.core.security import Principal, require_role
from app.modules.audit.schemas import AuditEvent

router = APIRouter(tags=["audit"])


@router.get("/audit", response_model=Page[AuditEvent])
def list_audit(
    entity_type: str | None = None,
    limit: int = 50,
    offset: int = 0,
    _: Principal = Depends(require_role(Role.admin)),
) -> Page[AuditEvent]:
    items = [
        AuditEvent(
            id=ex.uid(8001),
            user_id=ex.ESTIMATOR_ID,
            user_name="Demo Estimator",
            entity_type="document",
            entity_id=ex.DOCUMENT_ID,
            action="document.uploaded",
            metadata={"version": 1},
            created_at=ex.NOW,
        ),
        AuditEvent(
            id=ex.uid(8002),
            user_id=ex.ESTIMATOR_ID,
            user_name="Demo Estimator",
            entity_type="boq_item",
            entity_id=ex.uid(2001),
            action="boq_item.approved",
            metadata={},
            created_at=ex.NOW,
        ),
    ]
    return Page(items=items, total=len(items))
