"""Requirements, tasks and checklist. STARTER STUBS. TODO(C3): real implementation."""

import uuid

from fastapi import APIRouter, Depends, status

from app.core import examples as ex
from app.core.models.enums import (
    ChecklistStatus,
    MandatoryStatus,
    ReviewStatus,
    Role,
    TaskStatus,
)
from app.core.schemas import COMPLIANCE_DISCLAIMER
from app.core.security import ANY_MEMBER, EDITORS, Principal, require_role
from app.modules.checklist.schemas import (
    Checklist,
    Requirement,
    RequirementUpdate,
    Task,
    TaskCreate,
    TaskUpdate,
)

router = APIRouter(tags=["checklist"])
ASSIGNERS = (*EDITORS, Role.project_manager)


def _req(
    n: int,
    typ: str,
    desc: str,
    ms: MandatoryStatus,
    page: int | None,
    rs: ReviewStatus,
    assignee: uuid.UUID | None = None,
    name: str | None = None,
    due: int | None = None,
) -> Requirement:
    return Requirement(
        id=ex.uid(3000 + n),
        tender_id=ex.TENDER_ID,
        requirement_type=typ,
        description=desc,
        mandatory_status=ms,
        original_description=desc,
        source_document_id=ex.DOCUMENT_ID if page else None,
        source_page=page,
        review_status=rs,
        checklist_status=ChecklistStatus.open,
        flags=[] if page else ["no_source"],
        assigned_to=assignee,
        assignee_name=name,
        due_at=ex.days(due) if due is not None else None,
    )


_REQS = [
    _req(
        1,
        "briefing_meeting",
        "Compulsory site briefing, 28 Oct 2026 10:00, Ward 7 hall",
        MandatoryStatus.mandatory,
        2,
        ReviewStatus.approved,
        ex.PM_ID,
        "Demo Project Manager",
        9,
    ),
    _req(
        2,
        "certificate",
        "Valid CIDB grading 3EP or higher",
        MandatoryStatus.mandatory,
        3,
        ReviewStatus.extracted,
    ),
    _req(
        3,
        "document",
        "Certificate of Compliance (CoC) on completion, SANS 10142-1",
        MandatoryStatus.mandatory,
        7,
        ReviewStatus.corrected,
        ex.ESTIMATOR_ID,
        "Demo Estimator",
        20,
    ),
    _req(
        4,
        "document",
        "Tax clearance PIN and CSD registration number",
        MandatoryStatus.mandatory,
        3,
        ReviewStatus.extracted,
    ),
    _req(
        5,
        "document",
        "B-BBEE certificate or sworn affidavit",
        MandatoryStatus.conditional,
        None,
        ReviewStatus.extracted,
    ),
]
_TASKS = [
    Task(
        id=ex.uid(4001),
        tender_id=ex.TENDER_ID,
        requirement_id=_REQS[0].id,
        title="Attend site briefing",
        description=None,
        assigned_to=ex.PM_ID,
        status=TaskStatus.todo,
        due_at=ex.days(9),
    ),
    Task(
        id=ex.uid(4002),
        tender_id=ex.TENDER_ID,
        requirement_id=_REQS[1].id,
        title="Upload current CIDB certificate",
        description=None,
        assigned_to=ex.ADMIN_ID,
        status=TaskStatus.in_progress,
        due_at=ex.days(-1),
    ),
]


@router.get("/tenders/{tender_id}/requirements", response_model=list[Requirement])
def list_requirements(
    tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> list[Requirement]:
    return _REQS


@router.patch("/requirements/{requirement_id}", response_model=Requirement)
def update_requirement(
    requirement_id: uuid.UUID,
    body: RequirementUpdate,
    _: Principal = Depends(require_role(*ASSIGNERS)),
) -> Requirement:
    # TODO(C3): project managers may only change assigned_to / due_at; editors everything.
    return _REQS[1].model_copy(update={"id": requirement_id, **body.model_dump(exclude_none=True)})


@router.get("/tenders/{tender_id}/checklist", response_model=Checklist)
def get_checklist(
    tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> Checklist:
    return Checklist(
        tender_id=tender_id,
        disclaimer=COMPLIANCE_DISCLAIMER,
        requirements=_REQS,
        tasks=_TASKS,
        open_mandatory=4,
        overdue=1,
    )


@router.get("/tenders/{tender_id}/tasks", response_model=list[Task])
def list_tasks(
    tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> list[Task]:
    return _TASKS


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate, _: Principal = Depends(require_role(*ASSIGNERS))) -> Task:
    return Task(id=ex.uid(4100), status=TaskStatus.todo, **body.model_dump())


@router.patch("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: uuid.UUID, body: TaskUpdate, _: Principal = Depends(require_role(*ASSIGNERS))
) -> Task:
    return _TASKS[0].model_copy(update={"id": task_id, **body.model_dump(exclude_none=True)})
