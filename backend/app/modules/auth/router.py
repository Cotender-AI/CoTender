"""Auth endpoints. STARTER STUBS returning example data. TODO(A1): real implementation."""

import uuid

from fastapi import APIRouter, Depends, Response, status

from app.core import examples as ex
from app.core.models.enums import MembershipStatus, Role
from app.core.security import ANY_MEMBER, Principal, require_role
from app.modules.auth.schemas import (
    InviteRequest,
    InviteResponse,
    LoginRequest,
    Member,
    MemberUpdate,
    MeResponse,
    OrganisationSummary,
    RegisterRequest,
)

router = APIRouter(tags=["auth"])

_ME = MeResponse(
    id=ex.ADMIN_ID,
    email="admin@demo.co.za",
    name="Demo Admin",
    role=Role.admin,
    is_platform_admin=False,
    organisation=OrganisationSummary(id=ex.ORG_ID, name="Demo Electrical"),
)
_MEMBERS = [
    Member(
        id=ex.uid(1001),
        user_id=ex.ADMIN_ID,
        name="Demo Admin",
        email="admin@demo.co.za",
        role=Role.admin,
        status=MembershipStatus.active,
    ),
    Member(
        id=ex.uid(1002),
        user_id=ex.ESTIMATOR_ID,
        name="Demo Estimator",
        email="estimator@demo.co.za",
        role=Role.estimator,
        status=MembershipStatus.active,
    ),
    Member(
        id=ex.uid(1003),
        user_id=ex.PM_ID,
        name="Demo Project Manager",
        email="pm@demo.co.za",
        role=Role.project_manager,
        status=MembershipStatus.active,
    ),
    Member(
        id=ex.uid(1004),
        user_id=ex.REVIEWER_ID,
        name="Demo Reviewer",
        email="reviewer@demo.co.za",
        role=Role.reviewer,
        status=MembershipStatus.active,
    ),
]


@router.post("/auth/register", response_model=MeResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest) -> MeResponse:
    return _ME  # TODO(A1): create org + admin membership, set cookies


@router.post("/auth/login", response_model=MeResponse)
def login(body: LoginRequest, response: Response) -> MeResponse:
    return _ME  # TODO(A1): verify argon2id hash, set httpOnly access + refresh cookies


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    return None  # TODO(A1): clear cookies


@router.get("/me", response_model=MeResponse)
def me(_: Principal = Depends(require_role(*ANY_MEMBER))) -> MeResponse:
    return _ME


@router.get("/members", response_model=list[Member])
def list_members(_: Principal = Depends(require_role(*ANY_MEMBER))) -> list[Member]:
    return _MEMBERS


@router.post("/invites", response_model=InviteResponse, status_code=status.HTTP_201_CREATED)
def invite(body: InviteRequest, _: Principal = Depends(require_role(Role.admin))) -> InviteResponse:
    return InviteResponse(id=ex.uid(1100), email=body.email, role=body.role, expires_at=ex.days(7))


@router.patch("/members/{member_id}", response_model=Member)
def update_member(
    member_id: uuid.UUID, body: MemberUpdate, _: Principal = Depends(require_role(Role.admin))
) -> Member:
    m = _MEMBERS[1]
    return m.model_copy(update={k: v for k, v in body.model_dump().items() if v is not None})
