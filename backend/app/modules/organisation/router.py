"""Organisation settings. STARTER STUBS. TODO(A1): real implementation (admin edits)."""

from decimal import Decimal

from fastapi import APIRouter, Depends

from app.core import examples as ex
from app.core.models.enums import Role, VatMode
from app.core.security import ANY_MEMBER, Principal, require_role
from app.modules.organisation.schemas import Organisation, OrganisationUpdate

router = APIRouter(tags=["organisation"])

_ORG = Organisation(
    id=ex.ORG_ID,
    name="Demo Electrical (Pty) Ltd",
    registration_number=None,
    contact_email="admin@demo.co.za",
    plan="trial",
    currency="ZAR",
    vat_mode=VatMode.exclusive,
    vat_rate_pct=Decimal("15.00"),
    default_markup_pct=Decimal("12.50"),
)


@router.get("/organisation", response_model=Organisation)
def get_organisation(_: Principal = Depends(require_role(*ANY_MEMBER))) -> Organisation:
    return _ORG


@router.patch("/organisation", response_model=Organisation)
def update_organisation(
    body: OrganisationUpdate, _: Principal = Depends(require_role(Role.admin))
) -> Organisation:
    return _ORG.model_copy(update=body.model_dump(exclude_none=True))
