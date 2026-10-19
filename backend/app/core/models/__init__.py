"""All 20 tables. Import from here so Alembic sees every model."""

from app.core.models.base import Base
from app.core.models.documents import Document, DocumentPage, ExtractionJob
from app.core.models.extraction import BoqItem, FieldRevision, TenderRequirement
from app.core.models.identity import Invite, Membership, Organisation, User
from app.core.models.platform import AuditEvent, Export, Notification, UsageCounter
from app.core.models.suppliers import (
    QuoteMatch,
    Supplier,
    SupplierQuotation,
    SupplierQuotationItem,
)
from app.core.models.tenders import Task, Tender

__all__ = [
    "AuditEvent",
    "Base",
    "BoqItem",
    "Document",
    "DocumentPage",
    "Export",
    "ExtractionJob",
    "FieldRevision",
    "Invite",
    "Membership",
    "Notification",
    "Organisation",
    "QuoteMatch",
    "Supplier",
    "SupplierQuotation",
    "SupplierQuotationItem",
    "Task",
    "Tender",
    "TenderRequirement",
    "UsageCounter",
    "User",
]
