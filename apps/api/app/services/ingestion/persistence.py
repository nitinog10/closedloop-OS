from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.canonical_event import CanonicalEvent
from app.schemas.event import CanonicalEventCreate


async def persist_canonical_events(db: AsyncSession, events: list[CanonicalEventCreate]) -> list[tuple[CanonicalEvent, bool]]:
    persisted: list[tuple[CanonicalEvent, bool]] = []

    for event in events:
        existing_stmt = select(CanonicalEvent).where(
            CanonicalEvent.organization_id == UUID(event.organization_id),
            CanonicalEvent.dedupe_key == event.dedupe_key,
        )
        existing = (await db.execute(existing_stmt)).scalar_one_or_none()
        if existing:
            persisted.append((existing, False))
            continue

        record = CanonicalEvent(
            organization_id=UUID(event.organization_id),
            source=event.source,
            source_event_id=event.source_event_id,
            source_url=event.source_url,
            event_type=event.event_type,
            actor_external_id=event.actor_external_id,
            channel_external_id=event.channel_external_id,
            title=event.title,
            content=event.content,
            event_metadata=event.metadata,
            importance_score=event.importance_score,
            dedupe_key=event.dedupe_key,
        )
        db.add(record)
        persisted.append((record, True))

    await db.commit()
    for item, _ in persisted:
        await db.refresh(item)
    return persisted
