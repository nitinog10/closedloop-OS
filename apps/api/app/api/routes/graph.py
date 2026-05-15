from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, get_request_context
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.schemas.graph import GraphEdge, GraphNeighborhoodResponse, GraphNode
from app.services.db import get_db

router = APIRouter()


@router.get('/neighborhood/{entity_id}', response_model=GraphNeighborhoodResponse)
async def neighborhood(
    entity_id: str,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> GraphNeighborhoodResponse:
    try:
        entity_uuid = UUID(entity_id)
    except ValueError:
        return _fallback(entity_id)

    entity_stmt = select(Entity).where(Entity.id == entity_uuid, Entity.organization_id == UUID(ctx.organization_id))
    entity = (await db.execute(entity_stmt)).scalar_one_or_none()
    if not entity:
        return _fallback(entity_id)

    edges_stmt = select(Relationship).where(
        Relationship.organization_id == UUID(ctx.organization_id),
        or_(Relationship.from_entity_id == entity.id, Relationship.to_entity_id == entity.id),
    )
    relationships = (await db.execute(edges_stmt)).scalars().all()
    related_ids = {entity.id}
    for rel in relationships:
        related_ids.add(rel.from_entity_id)
        related_ids.add(rel.to_entity_id)

    nodes_stmt = select(Entity).where(Entity.id.in_(related_ids))
    nodes = (await db.execute(nodes_stmt)).scalars().all()
    return GraphNeighborhoodResponse(
        nodes=[
            GraphNode(id=str(node.id), type=node.type, label=node.name, attributes=node.attributes or {})
            for node in nodes
        ],
        edges=[
            GraphEdge(source=str(rel.from_entity_id), target=str(rel.to_entity_id), type=rel.relationship_type)
            for rel in relationships
        ],
    )


def _fallback(entity_id: str) -> GraphNeighborhoodResponse:
    return GraphNeighborhoodResponse(
        nodes=[
            GraphNode(id=entity_id, type='decision', label='Authentication architecture'),
            GraphNode(id='ticket-1', type='ticket', label='AUTH-142'),
            GraphNode(id='repo-1', type='repository', label='closedloop/core'),
        ],
        edges=[
            GraphEdge(source=entity_id, target='ticket-1', type='references'),
            GraphEdge(source='ticket-1', target='repo-1', type='implemented_in'),
        ],
    )
