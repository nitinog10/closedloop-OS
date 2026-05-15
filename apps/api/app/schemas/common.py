from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TimestampedSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
