from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import and_, exists, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, get_request_context
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.schemas.graph import GraphEdge, GraphNeighborhoodResponse, GraphNode
from app.services.db import get_db

router = APIRouter()


@router.get(
    '/neighborhood/{entity_id}',
    response_model=GraphNeighborhoodResponse,
    summary="Get Entity Neighborhood",
    description="Retrieve the graph neighborhood around an entity with configurable depth",
    response_description="Nodes and edges in the entity's neighborhood"
)
async def neighborhood(
    entity_id: str,
    depth: int = 1,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> GraphNeighborhoodResponse:
    """
    Get the graph neighborhood around a specific entity.
    
    Performs breadth-first traversal to find all connected entities
    within the specified depth.
    
    Parameters:
    - entity_id: UUID of the entity to explore
    - depth: How many hops to traverse (1-3, default 1)
    
    Returns:
    - nodes: All entities in the neighborhood
    - edges: All relationships connecting them
    
    Use cases:
    - "Show me everything connected to this decision"
    - "What tickets are linked to this goal?"
    - "Who worked on this feature?"
    
    Requires authentication.
    """
    try:
        entity_uuid = UUID(entity_id)
    except ValueError:
        return GraphNeighborhoodResponse(nodes=[], edges=[])

    entity_stmt = select(Entity).where(Entity.id == entity_uuid, Entity.organization_id == UUID(ctx.organization_id))
    entity = (await db.execute(entity_stmt)).scalar_one_or_none()
    if not entity:
        return GraphNeighborhoodResponse(nodes=[], edges=[])

    max_depth = max(1, min(depth, 3))
    org_id = UUID(ctx.organization_id)

    frontier = {entity.id}
    related_ids = {entity.id}
    relationship_map: dict[str, Relationship] = {}

    for _ in range(max_depth):
        if not frontier:
            break
        edges_stmt = select(Relationship).where(
            Relationship.organization_id == org_id,
            or_(Relationship.from_entity_id.in_(frontier), Relationship.to_entity_id.in_(frontier)),
        )
        batch = (await db.execute(edges_stmt)).scalars().all()
        next_frontier: set[UUID] = set()
        for rel in batch:
            relationship_map[str(rel.id)] = rel
            if rel.from_entity_id not in related_ids:
                next_frontier.add(rel.from_entity_id)
            if rel.to_entity_id not in related_ids:
                next_frontier.add(rel.to_entity_id)
            related_ids.add(rel.from_entity_id)
            related_ids.add(rel.to_entity_id)
        frontier = next_frontier

    nodes_stmt = select(Entity).where(Entity.organization_id == org_id, Entity.id.in_(related_ids))
    nodes = list((await db.execute(nodes_stmt)).scalars().all())

    return GraphNeighborhoodResponse(
        nodes=[
            GraphNode(id=str(node.id), type=node.type, label=node.name, attributes=node.attributes or {})
            for node in nodes
        ],
        edges=[
            GraphEdge(source=str(rel.from_entity_id), target=str(rel.to_entity_id), type=rel.relationship_type)
            for rel in relationship_map.values()
        ],
    )


@router.get(
    '/unlinked-work',
    summary="Find Unlinked Work",
    description="Anomaly detection - find work items not connected to goals or customer requests",
    response_description="List of unlinked work items"
)
async def unlinked_work(
    limit: int = 50,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Detect unlinked work - a key closed-loop signal.
    
    Finds artifacts and tickets that have no relationship to:
    - Goals (aligns_with)
    - Customer requests (references)
    
    This indicates work happening without clear business justification,
    a common source of wasted effort.
    
    Parameters:
    - limit: Max results to return (1-200, default 50)
    
    Returns:
    - count: Number of unlinked items found
    - items: Entity details (id, type, name, attributes)
    
    Use cases:
    - "Show me engineering work with no customer demand"
    - "What are we building that's not tied to OKRs?"
    - Sprint retrospectives and planning
    
    Requires authentication.
    """
    org_id = UUID(ctx.organization_id)
    safe_limit = max(1, min(limit, 200))

    aligns_exists = exists(
        select(Relationship.id).where(
            and_(
                Relationship.organization_id == org_id,
                Relationship.from_entity_id == Entity.id,
                Relationship.relationship_type == 'aligns_with',
            )
        )
    )
    references_exists = exists(
        select(Relationship.id).where(
            and_(
                Relationship.organization_id == org_id,
                Relationship.from_entity_id == Entity.id,
                Relationship.relationship_type == 'references',
            )
        )
    )

    stmt = (
        select(Entity)
        .where(
            Entity.organization_id == org_id,
            Entity.type.in_(['artifact', 'ticket']),
            ~aligns_exists,
            ~references_exists,
        )
        .order_by(Entity.created_at.desc())
        .limit(safe_limit)
    )
    items = list((await db.execute(stmt)).scalars().all())
    return {
        'count': len(items),
        'items': [
            {
                'entity_id': str(item.id),
                'type': item.type,
                'name': item.name,
                'attributes': item.attributes or {},
            }
            for item in items
        ],
    }
