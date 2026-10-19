import uuid
from datetime import datetime

from app.core.models.enums import ExportKind
from app.core.schemas import ApiModel


class ExportCreate(ApiModel):
    kind: ExportKind
    draft: bool = True


class Export(ApiModel):
    id: uuid.UUID
    tender_id: uuid.UUID
    kind: ExportKind
    version: int
    is_draft: bool
    generated_at: datetime
    generated_by_name: str | None
