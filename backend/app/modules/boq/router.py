"""BoQ endpoints. STARTER STUBS. TODO(C2): editing + pricing; TODO(C3): approval."""

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends

from app.core import examples as ex
from app.core.models.enums import ReviewStatus
from app.core.security import ANY_MEMBER, EDITORS, Principal, require_role
from app.modules.boq.schemas import (
    BoqItem,
    BoqItemUpdate,
    BoqResponse,
    BoqTotals,
    BulkApproveRequest,
    BulkApproveResponse,
)

router = APIRouter(tags=["boq"])


def _line(
    n: int,
    item: str,
    desc: str,
    unit: str | None,
    qty: str | None,
    mat: str | None,
    lab: str | None,
    status: ReviewStatus,
    flags: list[str],
    page: int | None,
) -> BoqItem:
    q = Decimal(qty) if qty is not None else None
    m, la = (Decimal(mat) if mat else None), (Decimal(lab) if lab else None)
    price = (m or Decimal(0)) + (la or Decimal(0)) if (m or la) else None
    total = (q * price).quantize(Decimal("0.01")) if q is not None and price is not None else None
    return BoqItem(
        id=ex.uid(2000 + n),
        tender_id=ex.TENDER_ID,
        sort_order=n,
        section="2. Cabling",
        item_number=item,
        description=desc,
        unit=unit,
        quantity=q,
        material_unit_cost=m,
        labour_unit_cost=la,
        markup_pct=None,
        unit_price=price,
        line_total=total,
        original_item_number=item,
        original_description=desc,
        original_unit=unit,
        original_quantity=q,
        source_document_id=ex.DOCUMENT_ID if page else None,
        source_page=page,
        review_status=status,
        flags=flags,
        approved_at=ex.NOW if status == ReviewStatus.approved else None,
    )


_ITEMS = [
    _line(
        1,
        "2.1",
        "Supply and install 4mm² 3-core PVC SWA PVC cable in trench",
        "m",
        "120.000",
        "58.40",
        "22.00",
        ReviewStatus.approved,
        [],
        14,
    ),
    _line(
        2,
        "2.2",
        "Supply and install 16mm² 4-core Cu PVC SWA PVC cable",
        "m",
        "45.000",
        "312.75",
        "41.50",
        ReviewStatus.corrected,
        [],
        14,
    ),
    _line(
        3,
        "2.3",
        "Distribution board, 24-way, surface mounted, IP65",
        "no",
        "1.000",
        None,
        None,
        ReviewStatus.extracted,
        ["missing_price"],
        15,
    ),
    _line(
        4,
        "2.4",
        "LED bulkhead luminaire 18W IP65 vandal resistant",
        "no",
        None,
        None,
        None,
        ReviewStatus.extracted,
        ["missing_quantity"],
        15,
    ),
    _line(
        5,
        "2.5",
        "Earth electrode 1.5m copper bonded rod",
        None,
        "4.000",
        None,
        None,
        ReviewStatus.extracted,
        ["missing_unit", "no_source"],
        None,
    ),
]


@router.get("/tenders/{tender_id}/boq", response_model=BoqResponse)
def get_boq(tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))) -> BoqResponse:
    approved = [i for i in _ITEMS if i.review_status == ReviewStatus.approved]
    sub = sum((i.line_total or Decimal(0) for i in approved), Decimal("0.00"))
    vat = (sub * Decimal("0.15")).quantize(Decimal("0.01"))
    return BoqResponse(
        items=_ITEMS,
        totals=BoqTotals(
            approved_subtotal=sub,
            vat=vat,
            total=sub + vat,
            currency="ZAR",
            vat_mode="exclusive",
            approved_lines=len(approved),
            unapproved_lines=len(_ITEMS) - len(approved),
        ),
    )


@router.patch("/boq-items/{item_id}", response_model=BoqItem)
def update_boq_item(
    item_id: uuid.UUID, body: BoqItemUpdate, _: Principal = Depends(require_role(*EDITORS))
) -> BoqItem:
    # TODO(C2): keep original_*, write field_revisions, status -> corrected, recompute price.
    changes = body.model_dump(exclude_none=True)
    return _ITEMS[1].model_copy(
        update={"id": item_id, **changes, "review_status": ReviewStatus.corrected}
    )


@router.post("/tenders/{tender_id}/boq/approve", response_model=BulkApproveResponse)
def approve_boq(
    tender_id: uuid.UUID, body: BulkApproveRequest, _: Principal = Depends(require_role(*EDITORS))
) -> BulkApproveResponse:
    return BulkApproveResponse(approved=len(body.item_ids), skipped=[])
