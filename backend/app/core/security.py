"""Who is calling, and are they allowed to.

STARTER STUB: until block A1 lands, every request is treated as the seeded demo admin so the
frontend and other lanes can work. A1 replaces get_current_principal with JWT-cookie auth
(argon2id passwords, 30 min access / 7 day refresh, httpOnly + Secure + SameSite=Lax).
"""

import uuid
from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status

from app.core.models.enums import Role

# Fixed ids shared with scripts/seed.py so stubbed responses line up with the seed data.
DEMO_ORG_ID = uuid.UUID("00000000-0000-4000-8000-000000000001")
DEMO_ADMIN_ID = uuid.UUID("00000000-0000-4000-8000-000000000101")


@dataclass(frozen=True)
class Principal:
    user_id: uuid.UUID
    organisation_id: uuid.UUID  # only ever taken from the verified token
    role: Role
    is_platform_admin: bool = False


def get_current_principal() -> Principal:
    # TODO(A1): read and verify the access-token cookie; raise 401 when missing or invalid.
    return Principal(user_id=DEMO_ADMIN_ID, organisation_id=DEMO_ORG_ID, role=Role.admin)


def require_role(*allowed: Role) -> Callable[[Principal], Principal]:
    """Dependency: 403 unless the caller has one of the allowed roles."""

    def check(principal: Principal = Depends(get_current_principal)) -> Principal:
        if principal.role not in allowed:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Your role cannot do this")
        return principal

    return check


ANY_MEMBER = (Role.admin, Role.estimator, Role.project_manager, Role.reviewer)
EDITORS = (Role.admin, Role.estimator)
