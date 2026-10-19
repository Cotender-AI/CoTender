import uuid
from datetime import datetime
from typing import Any

from app.core.schemas import ApiModel


class AuditEvent(ApiModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    user_name: str | None
    entity_type: str
    entity_id: uuid.UUID | None
    action: str
    metadata: dict[str, Any]
    created_at: datetime
