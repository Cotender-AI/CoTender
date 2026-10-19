import uuid
from datetime import datetime

from pydantic import EmailStr, Field

from app.core.models.enums import MembershipStatus, Role
from app.core.schemas import ApiModel


class RegisterRequest(ApiModel):
    organisation_name: str = Field(min_length=2, max_length=200)
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)


class LoginRequest(ApiModel):
    email: EmailStr
    password: str


class OrganisationSummary(ApiModel):
    id: uuid.UUID
    name: str


class MeResponse(ApiModel):
    id: uuid.UUID
    email: EmailStr
    name: str
    role: Role
    is_platform_admin: bool
    organisation: OrganisationSummary


class InviteRequest(ApiModel):
    email: EmailStr
    role: Role


class InviteResponse(ApiModel):
    id: uuid.UUID
    email: EmailStr
    role: Role
    expires_at: datetime


class Member(ApiModel):
    id: uuid.UUID  # membership id
    user_id: uuid.UUID
    name: str
    email: EmailStr
    role: Role
    status: MembershipStatus


class MemberUpdate(ApiModel):
    role: Role | None = None
    status: MembershipStatus | None = None
