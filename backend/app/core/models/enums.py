"""Status values. Stored as Postgres enums, so changing them needs a migration."""

import enum


class Role(enum.StrEnum):
    admin = "admin"
    estimator = "estimator"
    project_manager = "project_manager"
    reviewer = "reviewer"


class UserStatus(enum.StrEnum):
    active = "active"
    disabled = "disabled"


class MembershipStatus(enum.StrEnum):
    active = "active"
    deactivated = "deactivated"


class VatMode(enum.StrEnum):
    exclusive = "exclusive"  # prices exclude VAT, VAT added on top
    inclusive = "inclusive"  # prices already include VAT
    none = "none"  # not VAT registered


class TenderStatus(enum.StrEnum):
    draft = "draft"
    in_progress = "in_progress"
    ready = "ready"  # approved and ready for the contractor to submit themselves
    submitted = "submitted"  # recorded by a user; the system never submits bids
    archived = "archived"


class DocumentKind(enum.StrEnum):
    tender = "tender"
    supplier_quote = "supplier_quote"


class DocumentStatus(enum.StrEnum):
    uploaded = "uploaded"
    processing = "processing"
    processed = "processed"
    failed = "failed"
    superseded = "superseded"  # a newer version exists


class JobType(enum.StrEnum):
    tender_extraction = "tender_extraction"
    quote_extraction = "quote_extraction"


class JobStatus(enum.StrEnum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"


class ReviewStatus(enum.StrEnum):
    extracted = "extracted"
    corrected = "corrected"
    approved = "approved"
    rejected = "rejected"
    stale = "stale"


class MandatoryStatus(enum.StrEnum):
    mandatory = "mandatory"
    conditional = "conditional"
    optional = "optional"
    unclassified = "unclassified"


class ChecklistStatus(enum.StrEnum):
    open = "open"
    in_progress = "in_progress"
    done = "done"
    not_applicable = "not_applicable"


class MatchStatus(enum.StrEnum):
    suggested = "suggested"
    confirmed = "confirmed"
    rejected = "rejected"


class TaskStatus(enum.StrEnum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class ExportKind(enum.StrEnum):
    boq_excel = "boq_excel"
    checklist_pdf = "checklist_pdf"
