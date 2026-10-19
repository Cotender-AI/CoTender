import uuid
from datetime import datetime

from pydantic import Field

from app.core.models.enums import ChecklistStatus, MandatoryStatus, ReviewStatus, TaskStatus
from app.core.schemas import ApiModel


class Requirement(ApiModel):
    id: uuid.UUID
    tender_id: uuid.UUID
    requirement_type: str | None
    description: str
    mandatory_status: MandatoryStatus
    original_description: str | None
    source_document_id: uuid.UUID | None
    source_page: int | None
    review_status: ReviewStatus
    checklist_status: ChecklistStatus
    flags: list[str]
    assigned_to: uuid.UUID | None
    assignee_name: str | None
    due_at: datetime | None


class RequirementUpdate(ApiModel):
    description: str | None = None
    requirement_type: str | None = None
    mandatory_status: MandatoryStatus | None = None
    review_status: ReviewStatus | None = None
    checklist_status: ChecklistStatus | None = None
    assigned_to: uuid.UUID | None = None
    due_at: datetime | None = None


class Task(ApiModel):
    id: uuid.UUID
    tender_id: uuid.UUID
    requirement_id: uuid.UUID | None
    title: str
    description: str | None
    assigned_to: uuid.UUID | None
    status: TaskStatus
    due_at: datetime | None


class TaskCreate(ApiModel):
    tender_id: uuid.UUID
    requirement_id: uuid.UUID | None = None
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    assigned_to: uuid.UUID | None = None
    due_at: datetime | None = None


class TaskUpdate(ApiModel):
    title: str | None = None
    description: str | None = None
    assigned_to: uuid.UUID | None = None
    status: TaskStatus | None = None
    due_at: datetime | None = None


class Checklist(ApiModel):
    tender_id: uuid.UUID
    disclaimer: str
    requirements: list[Requirement]
    tasks: list[Task]
    open_mandatory: int
    overdue: int
