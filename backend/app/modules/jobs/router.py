"""Job status endpoints. STARTER STUBS. TODO(B1): real implementation. UI polls every 3 s."""

import uuid

from fastapi import APIRouter, Depends, status

from app.core import examples as ex
from app.core.models.enums import JobStatus, JobType
from app.core.security import ANY_MEMBER, EDITORS, Principal, require_role
from app.modules.jobs.schemas import Job

router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))) -> Job:
    return Job(
        id=job_id,
        document_id=ex.DOCUMENT_ID,
        job_type=JobType.tender_extraction,
        status=JobStatus.succeeded,
        attempt_count=1,
        error_code=None,
        started_at=ex.NOW,
        completed_at=ex.NOW,
    )


@router.post("/jobs/{job_id}/retry", response_model=Job, status_code=status.HTTP_202_ACCEPTED)
def retry_job(job_id: uuid.UUID, _: Principal = Depends(require_role(*EDITORS))) -> Job:
    return Job(
        id=job_id,
        document_id=ex.DOCUMENT_ID,
        job_type=JobType.tender_extraction,
        status=JobStatus.queued,
        attempt_count=1,
        error_code=None,
        started_at=None,
        completed_at=None,
    )
