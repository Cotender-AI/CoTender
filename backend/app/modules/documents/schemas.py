import uuid
from datetime import datetime

from app.core.models.enums import DocumentKind, DocumentStatus
from app.core.schemas import ApiModel, Timestamps


class Document(Timestamps):
    id: uuid.UUID
    tender_id: uuid.UUID
    kind: DocumentKind
    filename: str
    version: int
    mime_type: str
    file_size: int
    page_count: int | None
    checksum_sha256: str
    processing_status: DocumentStatus
    latest_job_id: uuid.UUID | None = None


class UploadAccepted(ApiModel):
    document: Document
    job_id: uuid.UUID


class DownloadLink(ApiModel):
    url: str
    expires_at: datetime
