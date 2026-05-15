import uuid

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import TimestampMixin, UUIDMixin
from app.services.db import Base


class Entity(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "entities"

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), index=True)
    type: Mapped[str] = mapped_column(String(100), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    external_key: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    attributes: Mapped[dict] = mapped_column(JSON, default=dict)
