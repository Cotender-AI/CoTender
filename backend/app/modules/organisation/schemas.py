import uuid

from pydantic import Field

from app.core.models.enums import VatMode
from app.core.schemas import ApiModel, DecimalStr


class Organisation(ApiModel):
    id: uuid.UUID
    name: str
    registration_number: str | None
    contact_email: str | None
    plan: str
    currency: str
    vat_mode: VatMode
    vat_rate_pct: DecimalStr
    default_markup_pct: DecimalStr


class OrganisationUpdate(ApiModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    registration_number: str | None = None
    contact_email: str | None = None
    vat_mode: VatMode | None = None
    vat_rate_pct: DecimalStr | None = None
    default_markup_pct: DecimalStr | None = None
