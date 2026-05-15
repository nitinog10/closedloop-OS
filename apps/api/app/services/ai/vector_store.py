from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.embedding import Embedding


class VectorStoreService:
    async def upsert_embedding(
        self,
        db: AsyncSession,
        organization_id: str,
        event_id: str,
        vector: list[float],
        model: str,
    ) -> Embedding:
        stmt = select(Embedding).where(Embedding.event_id == UUID(event_id))
        record = (await db.execute(stmt)).scalar_one_or_none()
        if record:
            record.model = model
            record.dimensions = len(vector)
            record.vector = vector
        else:
            record = Embedding(
                organization_id=UUID(organization_id),
                event_id=UUID(event_id),
                model=model,
                dimensions=len(vector),
                vector=vector,
            )
            db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    async def nearest_event_ids(
        self,
        db: AsyncSession,
        organization_id: str,
        query_vector: list[float],
        limit: int = 8,
    ) -> list[str]:
        try:
            result = await db.execute(
                text(
                    """
                    SELECT event_id::text
                    FROM embeddings
                    WHERE organization_id = :organization_id::uuid
                      AND vector IS NOT NULL
                    ORDER BY vector <=> :vector::vector
                    LIMIT :limit
                    """
                ),
                {
                    'organization_id': organization_id,
                    'vector': self._to_pgvector(query_vector),
                    'limit': limit,
                },
            )
            return [row.event_id for row in result]
        except Exception:
            return []

    def _to_pgvector(self, vector: list[float]) -> str:
        return '[' + ','.join(f'{value:.8f}' for value in vector) + ']'
