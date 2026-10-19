"""In-app notifications. STARTER STUB. TODO(A5-NOTIFY): real implementation + daily reminders."""

from fastapi import APIRouter, Depends

from app.core import examples as ex
from app.core.security import ANY_MEMBER, Principal, require_role
from app.modules.notifications.schemas import Notification

router = APIRouter(tags=["notifications"])


@router.get("/notifications", response_model=list[Notification])
def list_notifications(
    unread_only: bool = False, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> list[Notification]:
    return [
        Notification(
            id=ex.uid(9001),
            kind="tender_closing",
            title="RFQ ELEC-2026-131 closes in 9 days",
            body=None,
            entity_type="tender",
            entity_id=ex.uid(202),
            read=False,
            created_at=ex.NOW,
        )
    ]
