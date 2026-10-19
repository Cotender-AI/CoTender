import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base, IdMixin, OrgMixin, TimestampMixin, fk
from app.core.models.enums import MembershipStatus, Role, UserStatus, VatMode


class Organisation(IdMixin, TimestampMixin, Base):
    __tablename__ = "organisations"

    name: Mapped[str] = mapped_column(String(200))
    registration_number: Mapped[str | None] = mapped_column(String(50))
    contact_email: Mapped[str | None] = mapped_column(String(320))
    # Plan limits are recorded only; there is no payment integration (FR-47..49).
    plan: Mapped[str] = mapped_column(String(30), server_default="trial")
    subscription_status: Mapped[str] = mapped_column(String(30), server_default="active")
    monthly_page_limit: Mapped[int] = mapped_column(Integer, server_default="200")
    monthly_export_limit: Mapped[int] = mapped_column(Integer, server_default="50")
    currency: Mapped[str] = mapped_column(String(3), server_default="ZAR")
    vat_mode: Mapped[VatMode] = mapped_column(
        Enum(VatMode, name="vat_mode"), server_default=VatMode.exclusive.value
    )
    vat_rate_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), server_default="15.00")
    default_markup_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), server_default="0.00")


class User(IdMixin, TimestampMixin, Base):
    """Global identity. Not tenant-owned: org access goes through memberships."""

    __tablename__ = "users"
    __table_args__ = (Index("uq_users_email_lower", text("lower(email)"), unique=True),)

    email: Mapped[str] = mapped_column(String(320))
    name: Mapped[str] = mapped_column(String(200))
    password_hash: Mapped[str] = mapped_column(String(255))
    is_platform_admin: Mapped[bool] = mapped_column(Boolean, server_default="false")
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"), server_default=UserStatus.active.value
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Membership(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "memberships"
    __table_args__ = (UniqueConstraint("organisation_id", "user_id"),)

    user_id: Mapped[uuid.UUID] = fk("users.id")
    role: Mapped[Role] = mapped_column(Enum(Role, name="member_role"))
    status: Mapped[MembershipStatus] = mapped_column(
        Enum(MembershipStatus, name="membership_status"),
        server_default=MembershipStatus.active.value,
    )


class Invite(IdMixin, OrgMixin, TimestampMixin, Base):
    __tablename__ = "invites"

    email: Mapped[str] = mapped_column(String(320))
    role: Mapped[Role] = mapped_column(Enum(Role, name="member_role"))
    token_hash: Mapped[str] = mapped_column(String(128), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    invited_by: Mapped[uuid.UUID | None] = fk("users.id", nullable=True, ondelete="SET NULL")
