import uuid
from datetime import date

from pydantic import EmailStr, Field

from app.core.models.enums import MatchStatus
from app.core.schemas import ApiModel, DecimalStr


class SupplierCreate(ApiModel):
    name: str = Field(min_length=1, max_length=200)
    contact_email: EmailStr | None = None
    contact_phone: str | None = None


class Supplier(ApiModel):
    id: uuid.UUID
    name: str
    contact_email: EmailStr | None
    contact_phone: str | None


class QuotationCreate(ApiModel):
    supplier_id: uuid.UUID
    tender_id: uuid.UUID
    document_id: uuid.UUID = Field(description="an uploaded document of kind supplier_quote")
    quotation_reference: str | None = None
    valid_until: date | None = None


class Quotation(ApiModel):
    id: uuid.UUID
    supplier_id: uuid.UUID
    tender_id: uuid.UUID | None
    document_id: uuid.UUID | None
    quotation_reference: str | None
    valid_until: date | None
    currency: str


class MatchEvidence(ApiModel):
    text_score: DecimalStr
    unit_match: bool
    spec_match: bool
    spec_conflicts: list[str]
    quote_valid: bool


class MatchOption(ApiModel):
    match_id: uuid.UUID
    supplier_name: str
    quote_description: str
    unit: str | None
    unit_price: DecimalStr | None
    valid_until: date | None
    score: DecimalStr
    status: MatchStatus
    evidence: MatchEvidence


class ComparisonRow(ApiModel):
    boq_item_id: uuid.UUID
    item_number: str | None
    description: str
    unit: str | None
    quantity: DecimalStr | None
    options: list[MatchOption]


class MatchUpdate(ApiModel):
    status: MatchStatus
    note: str | None = None
