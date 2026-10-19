"""Demo data: one organisation, one user per role, one tender.

    docker compose exec api python -m scripts.seed

Safe to run more than once. Ids match app/core/examples.py so the stubbed API and the
database describe the same demo workspace. Password for every demo user: DemoPass123!
"""

import uuid

from argon2 import PasswordHasher
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import examples as ex
from app.core.db import SessionLocal
from app.core.models import Membership, Organisation, Tender, User
from app.core.models.enums import Role, TenderStatus

DEMO_PASSWORD = "DemoPass123!"

USERS = [
    (ex.ADMIN_ID, "admin@demo.co.za", "Demo Admin", Role.admin),
    (ex.ESTIMATOR_ID, "estimator@demo.co.za", "Demo Estimator", Role.estimator),
    (ex.PM_ID, "pm@demo.co.za", "Demo Project Manager", Role.project_manager),
    (ex.REVIEWER_ID, "reviewer@demo.co.za", "Demo Reviewer", Role.reviewer),
]


def seed(session: Session) -> None:
    if session.get(Organisation, ex.ORG_ID) is None:
        session.add(
            Organisation(
                id=ex.ORG_ID, name="Demo Electrical (Pty) Ltd", contact_email="admin@demo.co.za"
            )
        )
        session.flush()

    password_hash = PasswordHasher().hash(DEMO_PASSWORD)
    for user_id, email, name, role in USERS:
        if session.get(User, user_id) is None:
            session.add(User(id=user_id, email=email, name=name, password_hash=password_hash))
            session.flush()
        exists = session.scalar(
            select(Membership.id).where(
                Membership.organisation_id == ex.ORG_ID, Membership.user_id == user_id
            )
        )
        if exists is None:
            session.add(
                Membership(id=uuid.uuid4(), organisation_id=ex.ORG_ID, user_id=user_id, role=role)
            )

    if session.get(Tender, ex.TENDER_ID) is None:
        session.add(
            Tender(
                id=ex.TENDER_ID,
                organisation_id=ex.ORG_ID,
                title="Electrical reticulation upgrade, Ward 7 community hall",
                reference_number="RFQ ELEC-2026-114",
                client_name="Kwena Valley Local Municipality (fictional)",
                location="Ward 7, Kwena Valley",
                closing_at=ex.CLOSING,
                status=TenderStatus.draft,
                created_by=ex.ESTIMATOR_ID,
            )
        )
    session.commit()


def main() -> None:
    with SessionLocal() as session:
        seed(session)
    print(f"Seeded demo org with {len(USERS)} users (password: {DEMO_PASSWORD}) and one tender.")


if __name__ == "__main__":
    main()
