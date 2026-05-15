from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.canonical_event import CanonicalEvent
from app.schemas.chat import CitationPayload
from app.services.ai.embeddings import EmbeddingService
from app.services.ai.vector_store import VectorStoreService


class RetrievalService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    async def semantic_search(self, db: AsyncSession, organization_id: str, query: str, limit: int = 8) -> list[CitationPayload]:
        org_uuid = UUID(str(organization_id))
        lexical_stmt = (
            select(CanonicalEvent)
            .where(CanonicalEvent.organization_id == org_uuid)
            .order_by(CanonicalEvent.importance_score.desc(), CanonicalEvent.created_at.desc())
            .limit(limit * 3)
        )
        lexical_rows = (await db.execute(lexical_stmt)).scalars().all()

        query_vector = await self.embedding_service.embed(query)
        vector_event_ids = await self.vector_store.nearest_event_ids(db, organization_id, query_vector, limit=limit * 3)
        vector_event_uuids = [UUID(event_id) for event_id in vector_event_ids]

        vector_rows: list[CanonicalEvent] = []
        if vector_event_uuids:
            vector_stmt = select(CanonicalEvent).where(CanonicalEvent.id.in_(vector_event_uuids))
            vector_rows = list((await db.execute(vector_stmt)).scalars().all())

        merged: dict[str, CanonicalEvent] = {str(item.id): item for item in lexical_rows}
        for item in vector_rows:
            merged[str(item.id)] = item

        ranked = sorted(
            merged.values(),
            key=lambda item: self._hybrid_score(query, item, vector_event_ids),
            reverse=True,
        )[:limit]

        return [
            CitationPayload(
                event_id=str(row.id),
                source_type=row.source,
                source_title=row.title or f"{row.source} {row.event_type}",
                source_url=row.source_url,
                quote=(row.content[:280] + "...") if len(row.content) > 280 else row.content,
                relevance_score=float(self._hybrid_score(query, row, vector_event_ids)),
            )
            for row in ranked
        ]

    def _hybrid_score(self, query: str, item: CanonicalEvent, vector_event_ids: list[str]) -> float:
        lexical = self._keyword_overlap(query, item.content) + self._keyword_overlap(query, item.title or '')
        vector_bonus = 0.35 if str(item.id) in vector_event_ids else 0.0
        recency_bonus = 0.05
        return item.importance_score + lexical + vector_bonus + recency_bonus

    def _keyword_overlap(self, query: str, text: str) -> float:
        q_terms = {term.strip().lower() for term in query.split() if term.strip()}
        t_terms = {term.strip(".,:;!?()[]{}").lower() for term in text.split() if term.strip()}
        if not q_terms or not t_terms:
            return 0.0
        overlap = len(q_terms & t_terms)
        return min(overlap / max(len(q_terms), 1), 1.0)
