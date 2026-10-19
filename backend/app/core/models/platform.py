import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base, IdMixin, OrgMixin, TimestampMixin, fk
from app.core.models.enums import ExportKind


class Export(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "exports"
    __table_args__ = (
        Index("ix_exports_org_tender", "organisation_id", "tender_id"),
        UniqueConstraint("tender_id", "kind", "version"),
    )

    tender_id: Mapped[uuid.UUID] = fk("tenders.id")
    kind: Mapped[ExportKind] = mapped_column(Enum(ExportKind, name="export_kind"))
    version: Mapped[int] = mapped_column(Integer)
    is_draft: Mapped[bool] = mapped_column(Boolean, server_default="true")  # drafts watermarked
    storage_key: Mapped[str | None] = mapped_column(String(500))
    generated_by: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class AuditEvent(IdMixin, OrgMixin, Base):
    """Append-only. Ids and action names only, never document content."""

    __tablename__ = "audit_events"
    __table_args__ = (Index("ix_audit_events_org_created", "organisation_id", "created_at"),)

    user_id: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
    entity_type: Mapped[str] = mapped_column(String(50))
    entity_id: Mapped[uuid.UUID | None]
    action: Mapped[str] = mapped_column(String(100))
    request_id: Mapped[str | None] = mapped_column(String(64))
    # "metadata" is reserved on SQLAlchemy models, so the attribute is meta.
    meta: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, server_default=text("'{}'::jsonb")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Notification(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "notifications"
    __table_args__ = (Index("ix_notifications_user_read", "user_id", "read"),)

    user_id: Mapped[uuid.UUID] = fk("users.id")
    kind: Mapped[str] = mapped_column(String(50))  # tender_closing, task_due, job_failed, ...
    title: Mapped[str] = mapped_column(String(300))
    body: Mapped[str | None] = mapped_column(Text)
    entity_type: Mapped[str | None] = mapped_column(String(50))
    entity_id: Mapped[uuid.UUID | None]
    read: Mapped[bool] = mapped_column(Boolean, server_default="false")


class UsageCounter(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "usage_counters"
    __table_args__ = (UniqueConstraint("organisation_id", "period"),)

    period: Mapped[str] = mapped_column(String(7))  # YYYY-MM
    documents_uploaded: Mapped[int] = mapped_column(Integer, server_default="0")
    pages_processed: Mapped[int] = mapped_column(Integer, server_default="0")
    exports: Mapped[int] = mapped_column(Integer, server_default="0")
    llm_tokens: Mapped[int] = mapped_column(Integer, server_default="0")
