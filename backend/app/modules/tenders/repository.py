"""Template for every module: repositories inherit OrgScopedRepository and hold all SQL."""

from app.core.models import Tender
from app.core.repository import OrgScopedRepository


class TenderRepository(OrgScopedRepository[Tender]):
    model = Tender

    # TODO(C1): search + status filter, closing-soon query for the dashboard.
