"""Tender endpoints. STARTER STUBS returning example data. TODO(C1): real implementation."""

import uuid

from fastapi import APIRouter, Depends, Query, status

from app.core import examples as ex
from app.core.models.enums import Role, TenderStatus
from app.core.schemas import Page
from app.core.security import ANY_MEMBER, EDITORS, Principal, require_role
from app.modules.tenders.schemas import (
    Dashboard,
    DashboardTender,
    Tender,
    TenderCreate,
    TenderUpdate,
)

router = APIRouter(tags=["tenders"])

_TENDER = Tender(
    id=ex.TENDER_ID,
    title="Electrical reticulation upgrade, Ward 7 community hall",
    reference_number="RFQ ELEC-2026-114",
    client_name="Kwena Valley Local Municipality (fictional)",
    location="Ward 7, Kwena Valley",
    trade="electrical",
    closing_at=ex.CLOSING,
    status=TenderStatus.in_progress,
    created_at=ex.NOW,
    updated_at=ex.NOW,
)
_TENDER_2 = _TENDER.model_copy(
    update={
        "id": ex.uid(202),
        "title": "LED street lighting retrofit, Phase 2",
        "reference_number": "RFQ ELEC-2026-131",
        "closing_at": ex.days(9),
        "status": TenderStatus.draft,
    }
)
PM_EDITORS = (*EDITORS, Role.project_manager)


@router.post("/tenders", response_model=Tender, status_code=status.HTTP_201_CREATED)
def create_tender(body: TenderCreate, _: Principal = Depends(require_role(*EDITORS))) -> Tender:
    return _TENDER.model_copy(update={**body.model_dump(), "status": TenderStatus.draft})


@router.get("/tenders", response_model=Page[Tender])
def list_tenders(
    q: str | None = None,
    status_filter: TenderStatus | None = Query(default=None, alias="status"),
    include_archived: bool = False,
    _: Principal = Depends(require_role(*ANY_MEMBER)),
) -> Page[Tender]:
    return Page(items=[_TENDER, _TENDER_2], total=2)


@router.get("/tenders/{tender_id}", response_model=Tender)
def get_tender(tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))) -> Tender:
    return _TENDER.model_copy(update={"id": tender_id})


@router.patch("/tenders/{tender_id}", response_model=Tender)
def update_tender(
    tender_id: uuid.UUID, body: TenderUpdate, _: Principal = Depends(require_role(*PM_EDITORS))
) -> Tender:
    return _TENDER.model_copy(update={"id": tender_id, **body.model_dump(exclude_none=True)})


@router.post("/tenders/{tender_id}/archive", response_model=Tender)
def archive_tender(
    tender_id: uuid.UUID, _: Principal = Depends(require_role(*PM_EDITORS))
) -> Tender:
    return _TENDER.model_copy(
        update={"id": tender_id, "status": TenderStatus.archived, "archived_at": ex.NOW}
    )


@router.get("/dashboard", response_model=Dashboard)
def dashboard(_: Principal = Depends(require_role(*ANY_MEMBER))) -> Dashboard:
    return Dashboard(
        closing_soon=[
            DashboardTender(
                id=t.id,
                title=t.title,
                reference_number=t.reference_number,
                closing_at=t.closing_at,
                days_left=(t.closing_at - ex.NOW).days,
                status=t.status,
            )
            for t in (_TENDER_2, _TENDER)
        ],
        open_tenders=2,
        items_awaiting_review=14,
        overdue_tasks=1,
    )
