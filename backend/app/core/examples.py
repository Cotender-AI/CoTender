"""Fixed ids and timestamps used by the stubbed routers (and matched by scripts/seed.py)."""

import uuid
from datetime import UTC, datetime, timedelta

from app.core.security import DEMO_ADMIN_ID, DEMO_ORG_ID

ORG_ID = DEMO_ORG_ID
ADMIN_ID = DEMO_ADMIN_ID
ESTIMATOR_ID = uuid.UUID("00000000-0000-4000-8000-000000000102")
PM_ID = uuid.UUID("00000000-0000-4000-8000-000000000103")
REVIEWER_ID = uuid.UUID("00000000-0000-4000-8000-000000000104")
TENDER_ID = uuid.UUID("00000000-0000-4000-8000-000000000201")
DOCUMENT_ID = uuid.UUID("00000000-0000-4000-8000-000000000301")
JOB_ID = uuid.UUID("00000000-0000-4000-8000-000000000401")
SUPPLIER_ID = uuid.UUID("00000000-0000-4000-8000-000000000501")

NOW = datetime(2026, 10, 19, 9, 0, tzinfo=UTC)
CLOSING = datetime(2026, 11, 14, 9, 0, tzinfo=UTC)


def uid(n: int) -> uuid.UUID:
    return uuid.UUID(f"00000000-0000-4000-8000-{n:012d}")


def days(n: int) -> datetime:
    return NOW + timedelta(days=n)
