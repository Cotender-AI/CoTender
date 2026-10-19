import uuid
from datetime import datetime

from app.core.models.enums import JobStatus, JobType
from app.core.schemas import ApiModel


class Job(ApiModel):
    id: uuid.UUID
    document_id: uuid.UUID
    job_type: JobType
    status: JobStatus
    attempt_count: int
    error_code: str | None
    started_at: datetime | None
    completed_at: datetime | None
