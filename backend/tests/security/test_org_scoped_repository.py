"""Cross-tenant test (CLAUDE.md rule 2). Copy this pattern for every new resource."""

import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.core.models import Organisation, Tender
from app.modules.tenders.repository import TenderRepository


def _org(db: Session, name: str) -> Organisation:
    org = Organisation(id=uuid.uuid4(), name=name)
    db.add(org)
    db.flush()
    return org


def _tender(repo: TenderRepository, title: str) -> Tender:
    return repo.add(
        Tender(
            title=title,
            reference_number="RFQ-1",
            client_name="Client",
            closing_at=datetime(2026, 11, 14, tzinfo=UTC),
        )
    )


def test_org_b_cannot_read_update_or_delete_org_a_rows(db: Session) -> None:
    org_a, org_b = _org(db, "Org A"), _org(db, "Org B")
    repo_a, repo_b = TenderRepository(db, org_a.id), TenderRepository(db, org_b.id)
    tender_a = _tender(repo_a, "A's tender")

    assert repo_b.get(tender_a.id) is None
    with pytest.raises(NotFoundError):
        repo_b.get_or_404(tender_a.id)
    assert repo_b.list() == []
    assert repo_b.count() == 0
    assert repo_b.update(tender_a.id, title="hijacked") == 0
    assert repo_b.delete(tender_a.id) == 0

    db.expire_all()
    still_there = repo_a.get_or_404(tender_a.id)
    assert still_there.title == "A's tender"


def test_add_forces_the_callers_organisation(db: Session) -> None:
    org_a, org_b = _org(db, "Org A"), _org(db, "Org B")
    repo_b = TenderRepository(db, org_b.id)
    sneaky = Tender(
        organisation_id=org_a.id,
        title="x",
        reference_number="r",
        client_name="c",
        closing_at=datetime(2026, 11, 14, tzinfo=UTC),
    )
    with pytest.raises(ValueError):
        repo_b.add(sneaky)


def test_update_cannot_move_a_row_to_another_org(db: Session) -> None:
    org_a, org_b = _org(db, "Org A"), _org(db, "Org B")
    repo_a = TenderRepository(db, org_a.id)
    tender = _tender(repo_a, "mine")
    repo_a.update(tender.id, organisation_id=org_b.id, title="renamed")
    db.expire_all()
    assert repo_a.get_or_404(tender.id).organisation_id == org_a.id
