from datetime import datetime

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: str
    type: str
    title: str
    body: str
    severity: str
    payload: dict
    created_at: datetime
