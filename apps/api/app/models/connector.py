import uuid

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import TimestampMixin, UUIDMixin
from app.services.db import Base


class Connector(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "connectors"

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), index=True)
    type: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[str] = mapped_column(String(50), default="connected")
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    encrypted_secret: Mapped[str | None] = mapped_column(String(1024), nullable=True)
