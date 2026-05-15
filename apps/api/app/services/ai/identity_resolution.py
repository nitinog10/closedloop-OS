from __future__ import annotations

import re
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity
from app.models.identity_alias import IdentityAlias


class IdentityResolutionService:
    def _normalize(self, value: str) -> str:
        return re.sub(r'[^a-z0-9]+', '-', value.strip().lower()).strip('-')

    async def resolve_person(
        self,
        db: AsyncSession,
        organization_id: UUID,
        source: str,
        external_id: str,
        display_name: str | None = None,
    ) -> Entity:
        alias_stmt = select(IdentityAlias).where(
            IdentityAlias.organization_id == organization_id,
            IdentityAlias.source == source,
            IdentityAlias.external_id == external_id,
        )
        alias = (await db.execute(alias_stmt)).scalar_one_or_none()
        if alias:
            entity_stmt = select(Entity).where(Entity.id == alias.entity_id)
            entity = (await db.execute(entity_stmt)).scalar_one()
            return entity

        normalized_key = self._normalize(display_name or external_id)
        entity_stmt = select(Entity).where(
            Entity.organization_id == organization_id,
            Entity.type == 'person',
            Entity.external_key == normalized_key,
        )
        entity = (await db.execute(entity_stmt)).scalar_one_or_none()
        if not entity:
            entity = Entity(
                organization_id=organization_id,
                type='person',
                name=display_name or external_id,
                external_key=normalized_key,
                attributes={'aliases': [external_id]},
            )
            db.add(entity)
            await db.flush()

        alias = IdentityAlias(
            organization_id=organization_id,
            entity_id=entity.id,
            source=source,
            external_id=external_id,
            display_name=display_name,
            confidence_score=0.95 if display_name else 0.85,
        )
        db.add(alias)
        await db.flush()
        return entity
