import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base, IdMixin, OrgMixin, TimestampMixin, fk
from app.core.models.enums import DocumentKind, DocumentStatus, JobStatus, JobType


class Document(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "documents"
    __table_args__ = (
        Index("ix_documents_org_tender", "organisation_id", "tender_id"),
        UniqueConstraint("tender_id", "filename", "version"),
    )

    tender_id: Mapped[uuid.UUID] = fk("tenders.id")
    kind: Mapped[DocumentKind] = mapped_column(
        Enum(DocumentKind, name="document_kind"), server_default=DocumentKind.tender.value
    )
    filename: Mapped[str] = mapped_column(String(255))
    version: Mapped[int] = mapped_column(Integer, server_default="1")
    previous_version_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL")
    )
    storage_key: Mapped[str] = mapped_column(String(500))  # org/{org}/tenders/{t}/{doc}/v{n}
    mime_type: Mapped[str] = mapped_column(String(100))  # sniffed from bytes, not the extension
    file_size: Mapped[int] = mapped_column(BigInteger)
    page_count: Mapped[int | None] = mapped_column(Integer)
    checksum_sha256: Mapped[str] = mapped_column(String(64))
    processing_status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus, name="document_status"), server_default=DocumentStatus.uploaded.value
    )
    uploaded_by: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")


class DocumentPage(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "document_pages"
    __table_args__ = (UniqueConstraint("document_id", "page_no"),)

    document_id: Mapped[uuid.UUID] = fk("documents.id")
    page_no: Mapped[int] = mapped_column(Integer)  # 1-based page, or sheet index for workbooks
    sheet_name: Mapped[str | None] = mapped_column(String(100))
    text: Mapped[str | None] = mapped_column(Text)
    ocr_used: Mapped[bool] = mapped_column(Boolean, server_default="false")
    ocr_confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))


class ExtractionJob(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "extraction_jobs"
    __table_args__ = (Index("ix_extraction_jobs_org_document", "organisation_id", "document_id"),)

    document_id: Mapped[uuid.UUID] = fk("documents.id")
    job_type: Mapped[JobType] = mapped_column(Enum(JobType, name="job_type"))
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus, name="job_status"), server_default=JobStatus.queued.value
    )
    attempt_count: Mapped[int] = mapped_column(Integer, server_default="0")
    # document id + checksum + job type; unique so a retry never runs twice (rule 7)
    idempotency_key: Mapped[str] = mapped_column(String(200), unique=True)
    error_code: Mapped[str | None] = mapped_column(String(100))
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    llm_tokens_used: Mapped[int] = mapped_column(Integer, server_default="0")
