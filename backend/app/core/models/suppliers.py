import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base, IdMixin, OrgMixin, TimestampMixin, fk
from app.core.models.enums import MatchStatus, ReviewStatus
from app.core.models.extraction import ReviewFields, review_enum


class Supplier(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "suppliers"
    __table_args__ = (UniqueConstraint("organisation_id", "name"),)

    name: Mapped[str] = mapped_column(String(200))
    contact_email: Mapped[str | None] = mapped_column(String(320))
    contact_phone: Mapped[str | None] = mapped_column(String(50))


class SupplierQuotation(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "supplier_quotations"
    __table_args__ = (Index("ix_supplier_quotations_org_tender", "organisation_id", "tender_id"),)

    supplier_id: Mapped[uuid.UUID] = fk("suppliers.id")
    tender_id: Mapped[uuid.UUID | None] = fk("tenders.id", nullable=True)
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"), unique=True
    )
    quotation_reference: Mapped[str | None] = mapped_column(String(100))
    quotation_date: Mapped[date | None] = mapped_column(Date)
    valid_until: Mapped[date | None] = mapped_column(Date)
    currency: Mapped[str] = mapped_column(String(3), server_default="ZAR")
    review_status: Mapped[ReviewStatus] = mapped_column(
        review_enum, server_default=ReviewStatus.extracted.value
    )
    created_by: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")


class SupplierQuotationItem(IdMixin, OrgMixin, TimestampMixin, ReviewFields, Base):
    __tablename__ = "supplier_quotation_items"

    quotation_id: Mapped[uuid.UUID] = fk("supplier_quotations.id")
    description: Mapped[str] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String(30))
    quantity: Mapped[Decimal | None] = mapped_column(Numeric(14, 3))
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    source_reference: Mapped[str | None] = mapped_column(String(100))  # line no. on the quote
    original_description: Mapped[str | None] = mapped_column(Text)
    original_unit: Mapped[str | None] = mapped_column(String(30))
    original_quantity: Mapped[Decimal | None] = mapped_column(Numeric(14, 3))
    original_unit_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))


class QuoteMatch(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "quote_matches"
    __table_args__ = (
        Index("ix_quote_matches_org_tender", "organisation_id", "tender_id"),
        UniqueConstraint("boq_item_id", "quote_item_id"),
        # Only one confirmed match per BoQ line; only confirmed matches feed prices (rule 10).
        Index(
            "uq_quote_matches_one_confirmed",
            "boq_item_id",
            unique=True,
            postgresql_where=text("status = 'confirmed'"),
        ),
    )

    tender_id: Mapped[uuid.UUID] = fk("tenders.id")
    boq_item_id: Mapped[uuid.UUID] = fk("boq_items.id")
    quote_item_id: Mapped[uuid.UUID] = fk("supplier_quotation_items.id")
    score: Mapped[Decimal] = mapped_column(Numeric(5, 2))  # 0-100
    evidence: Mapped[dict[str, Any]] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))
    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus, name="match_status"), server_default=MatchStatus.suggested.value
    )
    decided_by: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None] = mapped_column(Text)
