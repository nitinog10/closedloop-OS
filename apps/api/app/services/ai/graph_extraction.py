from __future__ import annotations

import re
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.canonical_event import CanonicalEvent
from app.models.decision import Decision
from app.models.entity import Entity
from app.models.goal import Goal
from app.models.relationship import Relationship
from app.models.ticket import Ticket
from app.services.ai.identity_resolution import IdentityResolutionService


TICKET_PATTERN = re.compile(r'\b([A-Z]{2,10}-\d{1,6})\b')
REPO_PATTERN = re.compile(r'\b([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)\b')
GOAL_PATTERN = re.compile(r'goal[:\s]+([^\n\r.]+)', re.IGNORECASE)
DECISION_PATTERN = re.compile(r'decision[:\s]+([^\n\r.]+)', re.IGNORECASE)


class GraphExtractionService:
    def __init__(self) -> None:
        self.identity_service = IdentityResolutionService()

    async def process_event(self, db: AsyncSession, event: CanonicalEvent) -> dict:
        org_id = UUID(str(event.organization_id))
        created_entities: list[str] = []
        created_relationships: list[str] = []

        actor = None
        if event.actor_external_id:
            actor = await self.identity_service.resolve_person(
                db=db,
                organization_id=org_id,
                source=event.source,
                external_id=event.actor_external_id,
                display_name=event.actor_external_id,
            )
            created_entities.append(str(actor.id))

        event_anchor = await self._upsert_entity(
            db,
            organization_id=org_id,
            entity_type='artifact',
            name=event.title or f'{event.source}:{event.source_event_id}',
            external_key=f'{event.source}:{event.source_event_id}',
            attributes={'source': event.source, 'event_id': str(event.id), 'event_type': event.event_type},
        )
        created_entities.append(str(event_anchor.id))

        if actor:
            relationship = await self._upsert_relationship(
                db,
                organization_id=org_id,
                from_entity_id=actor.id,
                to_entity_id=event_anchor.id,
                relationship_type='authored',
            )
            created_relationships.append(str(relationship.id))

        for ticket_key in sorted(set(TICKET_PATTERN.findall(f'{event.title or ""} {event.content}'))):
            ticket_record = await self._upsert_ticket(db, org_id, ticket_key, event)
            ticket_entity = await self._upsert_entity(
                db,
                organization_id=org_id,
                entity_type='ticket',
                name=ticket_key,
                external_key=ticket_key,
                attributes={'ticket_id': str(ticket_record.id), 'status': ticket_record.status},
            )
            created_entities.append(str(ticket_entity.id))
            rel = await self._upsert_relationship(
                db,
                organization_id=org_id,
                from_entity_id=event_anchor.id,
                to_entity_id=ticket_entity.id,
                relationship_type='references',
            )
            created_relationships.append(str(rel.id))

        repositories = set(REPO_PATTERN.findall(f'{event.title or ""} {event.content}'))
        metadata_repo = event.event_metadata.get('repository') if event.event_metadata else None
        if metadata_repo:
            repositories.add(metadata_repo)
        for repo in sorted(repositories):
            repo_entity = await self._upsert_entity(
                db,
                organization_id=org_id,
                entity_type='repository',
                name=repo,
                external_key=repo.lower(),
                attributes={'source': event.source},
            )
            created_entities.append(str(repo_entity.id))
            rel_type = 'implemented_in' if event.source == 'github' else 'mentioned'
            rel = await self._upsert_relationship(
                db,
                organization_id=org_id,
                from_entity_id=event_anchor.id,
                to_entity_id=repo_entity.id,
                relationship_type=rel_type,
            )
            created_relationships.append(str(rel.id))

        for match in DECISION_PATTERN.findall(event.content):
            decision = await self._upsert_decision(db, org_id, match.strip(), event.content)
            decision_entity = await self._upsert_entity(
                db,
                organization_id=org_id,
                entity_type='decision',
                name=decision.title,
                external_key=str(decision.id),
                attributes={'decision_id': str(decision.id), 'status': decision.status},
            )
            created_entities.append(str(decision_entity.id))
            rel = await self._upsert_relationship(
                db,
                organization_id=org_id,
                from_entity_id=decision_entity.id,
                to_entity_id=event_anchor.id,
                relationship_type='decided_in',
            )
            created_relationships.append(str(rel.id))

        for match in GOAL_PATTERN.findall(event.content):
            goal = await self._upsert_goal(db, org_id, match.strip())
            goal_entity = await self._upsert_entity(
                db,
                organization_id=org_id,
                entity_type='goal',
                name=goal.title,
                external_key=str(goal.id),
                attributes={'goal_id': str(goal.id), 'status': goal.status},
            )
            created_entities.append(str(goal_entity.id))
            rel = await self._upsert_relationship(
                db,
                organization_id=org_id,
                from_entity_id=event_anchor.id,
                to_entity_id=goal_entity.id,
                relationship_type='aligns_with',
            )
            created_relationships.append(str(rel.id))

        await db.commit()
        return {
            'event_id': str(event.id),
            'created_entities': list(dict.fromkeys(created_entities)),
            'created_relationships': list(dict.fromkeys(created_relationships)),
        }

    async def _upsert_entity(
        self,
        db: AsyncSession,
        organization_id: UUID,
        entity_type: str,
        name: str,
        external_key: str | None,
        attributes: dict,
    ) -> Entity:
        stmt = select(Entity).where(
            and_(
                Entity.organization_id == organization_id,
                Entity.type == entity_type,
                Entity.external_key == external_key,
            )
        )
        entity = (await db.execute(stmt)).scalar_one_or_none()
        if entity:
            entity.attributes = {**(entity.attributes or {}), **attributes}
            await db.flush()
            return entity

        entity = Entity(
            organization_id=organization_id,
            type=entity_type,
            name=name,
            external_key=external_key,
            attributes=attributes,
        )
        db.add(entity)
        await db.flush()
        return entity

    async def _upsert_relationship(
        self,
        db: AsyncSession,
        organization_id: UUID,
        from_entity_id: UUID,
        to_entity_id: UUID,
        relationship_type: str,
    ) -> Relationship:
        stmt = select(Relationship).where(
            Relationship.organization_id == organization_id,
            Relationship.from_entity_id == from_entity_id,
            Relationship.to_entity_id == to_entity_id,
            Relationship.relationship_type == relationship_type,
        )
        relationship = (await db.execute(stmt)).scalar_one_or_none()
        if relationship:
            return relationship

        relationship = Relationship(
            organization_id=organization_id,
            from_entity_id=from_entity_id,
            to_entity_id=to_entity_id,
            relationship_type=relationship_type,
        )
        db.add(relationship)
        await db.flush()
        return relationship

    async def _upsert_ticket(self, db: AsyncSession, organization_id: UUID, ticket_key: str, event: CanonicalEvent) -> Ticket:
        stmt = select(Ticket).where(Ticket.organization_id == organization_id, Ticket.external_id == ticket_key)
        ticket = (await db.execute(stmt)).scalar_one_or_none()
        if ticket:
            return ticket
        ticket = Ticket(
            organization_id=organization_id,
            external_id=ticket_key,
            title=ticket_key,
            description=event.content[:1000],
            status='linked',
        )
        db.add(ticket)
        await db.flush()
        return ticket

    async def _upsert_decision(self, db: AsyncSession, organization_id: UUID, title: str, summary: str) -> Decision:
        stmt = select(Decision).where(Decision.organization_id == organization_id, Decision.title == title)
        decision = (await db.execute(stmt)).scalar_one_or_none()
        if decision:
            return decision
        decision = Decision(organization_id=organization_id, title=title[:255], summary=summary[:4000], status='open')
        db.add(decision)
        await db.flush()
        return decision

    async def _upsert_goal(self, db: AsyncSession, organization_id: UUID, title: str) -> Goal:
        stmt = select(Goal).where(Goal.organization_id == organization_id, Goal.title == title)
        goal = (await db.execute(stmt)).scalar_one_or_none()
        if goal:
            return goal
        goal = Goal(organization_id=organization_id, title=title[:255], description=title[:4000], status='on_track')
        db.add(goal)
        await db.flush()
        return goal
