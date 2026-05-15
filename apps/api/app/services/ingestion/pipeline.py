from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.canonical_event import CanonicalEvent
from app.services.ai.embeddings import EmbeddingService
from app.services.ai.graph_extraction import GraphExtractionService
from app.services.ai.vector_store import VectorStoreService
from app.services.event_bus import EventBus, InMemoryEventBus
from app.services.ingestion.normalizer import normalize_event
from app.services.ingestion.persistence import persist_canonical_events
from app.services.notifications.service import NotificationService


class IngestionPipelineService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.graph_extraction_service = GraphExtractionService()
        self.vector_store_service = VectorStoreService()
        self.notification_service = NotificationService()
        self.event_bus: EventBus = InMemoryEventBus()

    async def ingest(self, db: AsyncSession, source: str, payload: dict, organization_id: str) -> dict:
        normalized = await normalize_event(source, payload, organization_id)
        persisted = await persist_canonical_events(db, normalized)

        embedding_count = 0
        graph_results: list[dict] = []
        for event in persisted:
            await self.event_bus.publish('canonical-events.normalized', {'event_id': str(event.id), 'source': source})
            vector = await self.embedding_service.embed(event.content)
            await self.vector_store_service.upsert_embedding(
                db=db,
                organization_id=organization_id,
                event_id=str(event.id),
                vector=vector,
                model=self.embedding_service.model_name,
            )
            embedding_count += 1
            await self.event_bus.publish('canonical-events.embedded', {'event_id': str(event.id), 'dimensions': len(vector)})
            graph_result = await self.graph_extraction_service.process_event(db, event)
            graph_results.append(graph_result)
            await self.event_bus.publish('knowledge-graph.upserted', graph_result)

        await self.notification_service.publish(
            db=db,
            organization_id=organization_id,
            notification_type='ingestion.completed',
            title=f'{source.title()} ingestion complete',
            body=f'Processed {len(persisted)} {source} event(s), generated {embedding_count} embedding(s), and refreshed graph intelligence.',
            severity='info',
            payload={'source': source, 'events': [str(event.id) for event in persisted]},
        )

        return {
            'accepted': len(persisted),
            'event_ids': [str(event.id) for event in persisted],
            'embeddings_generated': embedding_count,
            'graph_updates': graph_results,
        }

    async def reindex_organization(self, db: AsyncSession, organization_id: str, limit: int = 100) -> dict:
        stmt = (
            select(CanonicalEvent)
            .where(CanonicalEvent.organization_id == UUID(organization_id))
            .order_by(CanonicalEvent.created_at.desc())
            .limit(limit)
        )
        events = (await db.execute(stmt)).scalars().all()
        graph_results: list[dict] = []
        embeddings = 0

        for event in events:
            vector = await self.embedding_service.embed(event.content)
            await self.vector_store_service.upsert_embedding(
                db=db,
                organization_id=organization_id,
                event_id=str(event.id),
                vector=vector,
                model=self.embedding_service.model_name,
            )
            embeddings += 1
            graph_results.append(await self.graph_extraction_service.process_event(db, event))

        await self.notification_service.publish(
            db=db,
            organization_id=organization_id,
            notification_type='reindex.completed',
            title='Tenant reindex completed',
            body=f'Re-indexed {len(events)} event(s) for semantic retrieval and graph reasoning.',
            severity='info',
            payload={'events': [str(event.id) for event in events]},
        )

        return {
            'events_processed': len(events),
            'embeddings_generated': embeddings,
            'graph_updates': graph_results,
        }
