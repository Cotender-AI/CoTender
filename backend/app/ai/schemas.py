"""Candidate schemas: the exact shape the AI may return (frozen contract, block F3-A).

AI output that does not validate against these is rejected. Candidates only ever become
`extracted` items; a person approves them. Numbers are Decimal; the AI never computes totals.
"""

import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


class SourceRef(BaseModel):
    source_document_id: uuid.UUID
    source_page: int | None = Field(
        default=None, ge=1, description="1-based page; missing means the item is flagged no_source"
    )


class BoqLineCandidate(SourceRef):
    item_number: str | None = None
    section: str | None = None
    description: str = Field(min_length=1)
    unit: str | None = None
    quantity: Decimal | None = Field(default=None, description="null = missing, 0 = zero")
    unit_price: Decimal | None = None


class RequirementCandidate(SourceRef):
    requirement_type: str | None = Field(
        default=None, description="e.g. deadline, briefing_meeting, document, certificate"
    )
    description: str = Field(min_length=1)
    mandatory_status: str = Field(
        default="unclassified", pattern="^(mandatory|conditional|optional|unclassified)$"
    )
    due_text: str | None = Field(default=None, description="date/time exactly as written")


class QuoteLineCandidate(SourceRef):
    description: str = Field(min_length=1)
    unit: str | None = None
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    source_reference: str | None = None


class BoqExtraction(BaseModel):
    items: list[BoqLineCandidate]


class RequirementExtraction(BaseModel):
    items: list[RequirementCandidate]


class QuoteExtraction(BaseModel):
    supplier_name: str | None = None
    quotation_reference: str | None = None
    valid_until: str | None = None
    items: list[QuoteLineCandidate]
