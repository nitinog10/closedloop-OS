from datetime import datetime
from pydantic import BaseModel


class CanonicalEventCreate(BaseModel):
    organization_id: str
    source: str
    source_event_id: str
    source_url: str | None = None
    event_type: str
    actor_external_id: str | None = None
    channel_external_id: str | None = None
    title: str | None = None
    content: str
    metadata: dict = {}
    importance_score: float = 0.5
    dedupe_key: str
    observed_at: datetime | None = None
