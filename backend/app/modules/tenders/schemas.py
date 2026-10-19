import uuid
from datetime import datetime

from pydantic import Field

from app.core.models.enums import TenderStatus
from app.core.schemas import ApiModel, Timestamps


class TenderCreate(ApiModel):
    title: str = Field(min_length=1, max_length=300)
    reference_number: str = Field(min_length=1, max_length=100)
    client_name: str = Field(min_length=1, max_length=200)
    location: str | None = Field(default=None, max_length=200)
    trade: str = "electrical"
    closing_at: datetime


class TenderUpdate(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    reference_number: str | None = None
    client_name: str | None = None
    location: str | None = None
    closing_at: datetime | None = None
    status: TenderStatus | None = None


class Tender(Timestamps):
    id: uuid.UUID
    title: str
    reference_number: str
    client_name: str
    location: str | None
    trade: str
    closing_at: datetime
    status: TenderStatus
    archived_at: datetime | None = None


class DashboardTender(ApiModel):
    id: uuid.UUID
    title: str
    reference_number: str
    closing_at: datetime
    days_left: int
    status: TenderStatus


class Dashboard(ApiModel):
    closing_soon: list[DashboardTender]
    open_tenders: int
    items_awaiting_review: int
    overdue_tasks: int
