"""Items the AI extracts. Live columns are editable; original_* keep what was extracted."""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base, IdMixin, OrgMixin, TimestampMixin, fk
from app.core.models.enums import ChecklistStatus, MandatoryStatus, ReviewStatus

review_enum = Enum(ReviewStatus, name="review_status")


class ReviewFields:
    """Shared provenance + review columns (rules 5, 6, 9)."""

    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL")
    )
    source_page: Mapped[int | None] = mapped_column(Integer)  # missing -> flag no_source
    extraction_job_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("extraction_jobs.id", ondelete="SET NULL")
    )
    review_status: Mapped[ReviewStatus] = mapped_column(
        review_enum, server_default=ReviewStatus.extracted.value
    )
    flags: Mapped[list[Any]] = mapped_column(JSONB, server_default=text("'[]'::jsonb"))
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TenderRequirement(IdMixin, OrgMixin, TimestampMixin, ReviewFields, Base):
    __tablename__ = "tender_requirements"
    __table_args__ = (Index("ix_tender_requirements_org_tender", "organisation_id", "tender_id"),)

    tender_id: Mapped[uuid.UUID] = fk("tenders.id")
    requirement_type: Mapped[str | None] = mapped_column(String(50))  # deadline, document, meeting
    description: Mapped[str] = mapped_column(Text)
    mandatory_status: Mapped[MandatoryStatus] = mapped_column(
        Enum(MandatoryStatus, name="mandatory_status"),
        server_default=MandatoryStatus.unclassified.value,
    )
    original_requirement_type: Mapped[str | None] = mapped_column(String(50))
    original_description: Mapped[str | None] = mapped_column(Text)
    original_mandatory_status: Mapped[MandatoryStatus | None] = mapped_column(
        Enum(MandatoryStatus, name="mandatory_status")
    )
    checklist_status: Mapped[ChecklistStatus] = mapped_column(
        Enum(ChecklistStatus, name="checklist_status"), server_default=ChecklistStatus.open.value
    )
    assigned_to: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class BoqItem(IdMixin, OrgMixin, TimestampMixin, ReviewFields, Base):
    __tablename__ = "boq_items"
    __table_args__ = (Index("ix_boq_items_org_tender", "organisation_id", "tender_id"),)

    tender_id: Mapped[uuid.UUID] = fk("tenders.id")
    sort_order: Mapped[int] = mapped_column(Integer, server_default="0")
    section: Mapped[str | None] = mapped_column(String(200))
    item_number: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String(30))
    quantity: Mapped[Decimal | None] = mapped_column(Numeric(14, 3))  # NULL = missing, 0 = zero
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    material_unit_cost: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    labour_unit_cost: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    markup_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))  # NULL = org default
    original_item_number: Mapped[str | None] = mapped_column(String(50))
    original_description: Mapped[str | None] = mapped_column(Text)
    original_unit: Mapped[str | None] = mapped_column(String(30))
    original_quantity: Mapped[Decimal | None] = mapped_column(Numeric(14, 3))
    original_unit_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))


class FieldRevision(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "field_revisions"
    __table_args__ = (
        Index("ix_field_revisions_entity", "organisation_id", "entity_type", "entity_id"),
    )

    tender_id: Mapped[uuid.UUID | None] = fk("tenders.id", nullable=True)
    entity_type: Mapped[str] = mapped_column(String(50))  # boq_item, tender_requirement, ...
    entity_id: Mapped[uuid.UUID]
    field: Mapped[str] = mapped_column(String(100))
    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
