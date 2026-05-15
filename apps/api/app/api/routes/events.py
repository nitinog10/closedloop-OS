from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.db import get_db
from app.services.ingestion.pipeline import IngestionPipelineService

router = APIRouter()
pipeline_service = IngestionPipelineService()


@router.post('/slack')
async def ingest_slack(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001'),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await pipeline_service.ingest(db=db, source='slack', payload=payload, organization_id=x_organization_id)


@router.post('/github')
async def ingest_github(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001'),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await pipeline_service.ingest(db=db, source='github', payload=payload, organization_id=x_organization_id)


@router.post('/linear')
async def ingest_linear(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001'),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await pipeline_service.ingest(db=db, source='linear', payload=payload, organization_id=x_organization_id)


@router.post('/notion')
async def ingest_notion(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001'),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await pipeline_service.ingest(db=db, source='notion', payload=payload, organization_id=x_organization_id)


@router.post('/zoom')
async def ingest_zoom(
    payload: dict,
    x_organization_id: str = Header(default='00000000-0000-0000-0000-000000000001'),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await pipeline_service.ingest(db=db, source='zoom', payload=payload, organization_id=x_organization_id)
