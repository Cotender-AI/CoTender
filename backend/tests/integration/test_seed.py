from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.models import Membership, Tender, User
from scripts.seed import seed


def test_seed_is_idempotent(db: Session) -> None:
    seed(db)
    seed(db)
    assert db.scalar(select(func.count()).select_from(User)) == 4
    assert db.scalar(select(func.count()).select_from(Membership)) == 4
    assert db.scalar(select(func.count()).select_from(Tender)) == 1
