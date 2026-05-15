import uuid

from sqlalchemy import Float, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import TimestampMixin, UUIDMixin
from app.services.db import Base


class CanonicalEvent(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "canonical_events"

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), index=True)
    connector_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("connectors.id"), nullable=True)
    source: Mapped[str] = mapped_column(String(50), index=True)
    source_event_id: Mapped[str] = mapped_column(String(255), index=True)
    source_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    actor_external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    channel_external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    event_metadata: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)
    dedupe_key: Mapped[str] = mapped_column(String(255), index=True)
