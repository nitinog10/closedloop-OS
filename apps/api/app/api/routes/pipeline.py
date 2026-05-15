from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, require_role
from app.services.db import get_db
from app.services.ingestion.pipeline import IngestionPipelineService

router = APIRouter()
pipeline_service = IngestionPipelineService()


@router.post('/reindex')
async def reindex(
    limit: int = 100,
    ctx: RequestContext = Depends(require_role('owner', 'admin')),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await pipeline_service.reindex_organization(db=db, organization_id=ctx.organization_id, limit=limit)
