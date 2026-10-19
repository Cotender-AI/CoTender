import uuid
from datetime import datetime

from app.core.schemas import ApiModel


class Notification(ApiModel):
    id: uuid.UUID
    kind: str
    title: str
    body: str | None
    entity_type: str | None
    entity_id: uuid.UUID | None
    read: bool
    created_at: datetime
