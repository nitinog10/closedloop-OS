from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, get_request_context
from app.services.ai.retrieval import RetrievalService
from app.services.ai.safety import SafetyService
from app.services.db import get_db

router = APIRouter()
retrieval_service = RetrievalService()
safety_service = SafetyService()


@router.post('/semantic')
async def semantic_search(
    payload: dict,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> dict:
    query = payload.get('query', '')
    safety_service.validate_query(query)
    results = await retrieval_service.semantic_search(db, ctx.organization_id, query, limit=payload.get('limit', 8))
    return {'results': [result.model_dump() for result in results]}
