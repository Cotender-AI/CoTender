import uuid
from datetime import datetime

from pydantic import Field

from app.core.models.enums import ReviewStatus
from app.core.schemas import ApiModel, DecimalStr


class BoqItem(ApiModel):
    id: uuid.UUID
    tender_id: uuid.UUID
    sort_order: int
    section: str | None
    item_number: str | None
    description: str
    unit: str | None
    quantity: DecimalStr | None = Field(description="null = missing, '0.000' = zero")
    material_unit_cost: DecimalStr | None
    labour_unit_cost: DecimalStr | None
    markup_pct: DecimalStr | None = Field(description="null = organisation default")
    unit_price: DecimalStr | None
    line_total: DecimalStr | None = Field(description="computed by the server, never the browser")
    original_item_number: str | None
    original_description: str | None
    original_unit: str | None
    original_quantity: DecimalStr | None
    source_document_id: uuid.UUID | None
    source_page: int | None
    review_status: ReviewStatus
    flags: list[str]
    approved_at: datetime | None


class BoqTotals(ApiModel):
    approved_subtotal: DecimalStr
    vat: DecimalStr
    total: DecimalStr
    currency: str
    vat_mode: str
    approved_lines: int
    unapproved_lines: int


class BoqResponse(ApiModel):
    items: list[BoqItem]
    totals: BoqTotals


class BoqItemUpdate(ApiModel):
    item_number: str | None = None
    description: str | None = None
    unit: str | None = None
    quantity: DecimalStr | None = None
    material_unit_cost: DecimalStr | None = None
    labour_unit_cost: DecimalStr | None = None
    markup_pct: DecimalStr | None = None
    review_status: ReviewStatus | None = Field(
        default=None, description="approved/rejected only via the review service"
    )


class BulkApproveRequest(ApiModel):
    item_ids: list[uuid.UUID] = Field(min_length=1)


class BulkApproveResponse(ApiModel):
    approved: int
    skipped: list[uuid.UUID] = Field(description="e.g. flagged no_source, cannot be approved")
