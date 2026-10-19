"""Suppliers, quotations, comparisons. STARTER STUBS. TODO(C4-API) + matcher TODO(C4-MATCH)."""

import uuid
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, status

from app.core import examples as ex
from app.core.models.enums import MatchStatus
from app.core.security import ANY_MEMBER, EDITORS, Principal, require_role
from app.modules.suppliers.schemas import (
    ComparisonRow,
    MatchEvidence,
    MatchOption,
    MatchUpdate,
    Quotation,
    QuotationCreate,
    Supplier,
    SupplierCreate,
)

router = APIRouter(tags=["suppliers"])

_SUPPLIERS = [
    Supplier(
        id=ex.SUPPLIER_ID,
        name="Voltline Wholesale (fictional)",
        contact_email="quotes@voltline.example",
        contact_phone=None,
    ),
    Supplier(
        id=ex.uid(502),
        name="Kwena Cables & Switchgear (fictional)",
        contact_email=None,
        contact_phone="+27 11 000 0000",
    ),
]


def _opt(
    n: int,
    supplier: str,
    desc: str,
    unit: str,
    price: str,
    score: str,
    unit_ok: bool,
    conflicts: list[str],
    st: MatchStatus,
) -> MatchOption:
    return MatchOption(
        match_id=ex.uid(6000 + n),
        supplier_name=supplier,
        quote_description=desc,
        unit=unit,
        unit_price=Decimal(price),
        valid_until=date(2026, 11, 30),
        score=Decimal(score),
        status=st,
        evidence=MatchEvidence(
            text_score=Decimal(score),
            unit_match=unit_ok,
            spec_match=not conflicts,
            spec_conflicts=conflicts,
            quote_valid=True,
        ),
    )


@router.post("/suppliers", response_model=Supplier, status_code=status.HTTP_201_CREATED)
def create_supplier(
    body: SupplierCreate, _: Principal = Depends(require_role(*EDITORS))
) -> Supplier:
    return Supplier(id=ex.uid(599), **body.model_dump())


@router.get("/suppliers", response_model=list[Supplier])
def list_suppliers(_: Principal = Depends(require_role(*ANY_MEMBER))) -> list[Supplier]:
    return _SUPPLIERS


@router.post("/quotations", response_model=Quotation, status_code=status.HTTP_201_CREATED)
def create_quotation(
    body: QuotationCreate, _: Principal = Depends(require_role(*EDITORS))
) -> Quotation:
    return Quotation(id=ex.uid(5100), currency="ZAR", **body.model_dump())


@router.get("/tenders/{tender_id}/comparisons", response_model=list[ComparisonRow])
def comparisons(
    tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> list[ComparisonRow]:
    return [
        ComparisonRow(
            boq_item_id=ex.uid(2002),
            item_number="2.2",
            description="Supply and install 16mm² 4-core Cu PVC SWA PVC cable",
            unit="m",
            quantity=Decimal("45.000"),
            options=[
                _opt(
                    1,
                    _SUPPLIERS[0].name,
                    "16mm 4C SWA PVC Cu cable per metre",
                    "m",
                    "289.90",
                    "91.50",
                    True,
                    [],
                    MatchStatus.suggested,
                ),
                _opt(
                    2,
                    _SUPPLIERS[1].name,
                    "16mm² 3-core SWA cable, 100m drum",
                    "drum",
                    "24150.00",
                    "78.00",
                    False,
                    ["cores: 4 vs 3"],
                    MatchStatus.suggested,
                ),
            ],
        )
    ]


@router.patch("/matches/{match_id}", response_model=MatchOption)
def update_match(
    match_id: uuid.UUID, body: MatchUpdate, _: Principal = Depends(require_role(*EDITORS))
) -> MatchOption:
    # TODO(C4-API): one confirmed per BoQ line; confirmed price feeds the line. Never auto-pick.
    return _opt(
        1,
        _SUPPLIERS[0].name,
        "16mm 4C SWA PVC Cu cable per metre",
        "m",
        "289.90",
        "91.50",
        True,
        [],
        body.status,
    ).model_copy(update={"match_id": match_id})
