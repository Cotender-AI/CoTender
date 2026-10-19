import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.ai.schemas import BoqLineCandidate, RequirementCandidate


def test_boq_candidate_keeps_null_quantity_distinct_from_zero() -> None:
    doc = uuid.uuid4()
    missing = BoqLineCandidate(source_document_id=doc, source_page=3, description="Cable")
    zero = BoqLineCandidate(
        source_document_id=doc, source_page=3, description="Cable", quantity=Decimal("0")
    )
    assert missing.quantity is None
    assert zero.quantity == Decimal("0")


def test_requirement_candidate_rejects_unknown_classification() -> None:
    with pytest.raises(ValidationError):
        RequirementCandidate(
            source_document_id=uuid.uuid4(),
            source_page=1,
            description="CIDB 3EP",
            mandatory_status="probably",
        )
