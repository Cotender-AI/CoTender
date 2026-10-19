import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base, IdMixin, OrgMixin, TimestampMixin, fk
from app.core.models.enums import TaskStatus, TenderStatus


class Tender(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "tenders"
    __table_args__ = (Index("ix_tenders_org_closing", "organisation_id", "closing_at"),)

    title: Mapped[str] = mapped_column(String(300))
    reference_number: Mapped[str] = mapped_column(String(100))
    client_name: Mapped[str] = mapped_column(String(200))
    location: Mapped[str | None] = mapped_column(String(200))
    trade: Mapped[str] = mapped_column(String(50), server_default="electrical")
    closing_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[TenderStatus] = mapped_column(
        Enum(TenderStatus, name="tender_status"), server_default=TenderStatus.draft.value
    )
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")


class Task(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (Index("ix_tasks_org_tender", "organisation_id", "tender_id"),)

    tender_id: Mapped[uuid.UUID] = fk("tenders.id")
    requirement_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tender_requirements.id", ondelete="SET NULL")
    )
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text)
    assigned_to: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"), server_default=TaskStatus.todo.value
    )
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
