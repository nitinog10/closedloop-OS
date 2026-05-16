from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.db import get_db
from app.services.ingestion.pipeline import IngestionPipelineService

router = APIRouter()
pipeline_service = IngestionPipelineService()


@router.post(
    '/slack',
    summary="Ingest Slack Event",
    description="Webhook endpoint for Slack events - processes messages, reactions, and channel activity",
    response_description="Ingestion result with event IDs and processing stats",
    responses={
        400: {"description": "Invalid payload or normalization error"}
    }
)
async def ingest_slack(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001', description="Organization ID for multi-tenant routing"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Ingest Slack events via webhook.
    
    Processes:
    - Messages (channel, DM, thread)
    - Reactions
    - File uploads
    - Channel events
    
    Automatically:
    - Normalizes to canonical event format
    - Generates embeddings for semantic search
    - Extracts entities and relationships
    - Publishes to event stream
    
    Returns processing statistics including event IDs and graph updates.
    """
    try:
        return await pipeline_service.ingest(db=db, source='slack', payload=payload, organization_id=x_organization_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    '/github',
    summary="Ingest GitHub Event",
    description="Webhook endpoint for GitHub events - processes PRs, issues, commits, and reviews",
    response_description="Ingestion result with event IDs and processing stats",
    responses={
        400: {"description": "Invalid payload or normalization error"}
    }
)
async def ingest_github(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001', description="Organization ID for multi-tenant routing"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Ingest GitHub events via webhook.
    
    Processes:
    - Pull requests (opened, merged, reviewed)
    - Issues (created, updated, closed)
    - Commits and pushes
    - Code reviews and comments
    
    Automatically links to Linear tickets and extracts technical decisions.
    """
    try:
        return await pipeline_service.ingest(db=db, source='github', payload=payload, organization_id=x_organization_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    '/linear',
    summary="Ingest Linear Event",
    description="Webhook endpoint for Linear events - processes issues, projects, and cycles",
    response_description="Ingestion result with event IDs and processing stats",
    responses={
        400: {"description": "Invalid payload or normalization error"}
    }
)
async def ingest_linear(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001', description="Organization ID for multi-tenant routing"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Ingest Linear events via webhook.
    
    Processes:
    - Issues (created, updated, status changes)
    - Projects and milestones
    - Cycles and sprints
    - Comments and attachments
    
    Automatically tracks goals and links to GitHub PRs.
    """
    try:
        return await pipeline_service.ingest(db=db, source='linear', payload=payload, organization_id=x_organization_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    '/notion',
    summary="Ingest Notion Event",
    description="Webhook endpoint for Notion events - processes pages, databases, and blocks",
    response_description="Ingestion result with event IDs and processing stats",
    responses={
        400: {"description": "Invalid payload or normalization error"}
    }
)
async def ingest_notion(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001', description="Organization ID for multi-tenant routing"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Ingest Notion events via webhook.
    
    Processes:
    - Page updates (docs, specs, ADRs)
    - Database changes
    - Block modifications
    
    Extracts decisions, goals, and architectural documentation.
    """
    try:
        return await pipeline_service.ingest(db=db, source='notion', payload=payload, organization_id=x_organization_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    '/zoom',
    summary="Ingest Zoom Event",
    description="Webhook endpoint for Zoom events - processes meeting transcripts and recordings",
    response_description="Ingestion result with event IDs and processing stats",
    responses={
        400: {"description": "Invalid payload or normalization error"}
    }
)
async def ingest_zoom(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001', description="Organization ID for multi-tenant routing"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Ingest Zoom events via webhook.
    
    Processes:
    - Meeting transcripts
    - Recording metadata
    - Participant information
    
    Extracts decisions and action items from meeting content.
    """
    try:
        return await pipeline_service.ingest(db=db, source='zoom', payload=payload, organization_id=x_organization_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
