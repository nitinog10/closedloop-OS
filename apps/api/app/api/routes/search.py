from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, get_request_context
from app.services.ai.retrieval import RetrievalService
from app.services.ai.safety import SafetyService
from app.services.db import get_db

router = APIRouter()
retrieval_service = RetrievalService()
safety_service = SafetyService()


@router.post(
    '/semantic',
    summary="Semantic Search",
    description="Search across all organizational data using semantic similarity",
    response_description="Ranked search results with relevance scores and citations",
    responses={
        400: {"description": "Invalid or unsafe query"}
    }
)
async def semantic_search(
    payload: dict,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Perform semantic search across all ingested events and documents.
    
    Uses hybrid retrieval combining:
    - Vector similarity (embeddings)
    - Lexical matching (keywords)
    - Importance scoring
    - Recency weighting
    
    Request body:
    ```json
    {
        "query": "What did we decide about authentication?",
        "limit": 8
    }
    ```
    
    Returns:
    - Ranked results with relevance scores
    - Source citations (Slack, GitHub, Linear, etc.)
    - Clickable links to original content
    - Quote excerpts
    
    Requires authentication.
    """
    query = payload.get('query', '')
    safety_service.validate_query(query)
    results = await retrieval_service.semantic_search(db, ctx.organization_id, query, limit=payload.get('limit', 8))
    return {'results': [result.model_dump() for result in results]}
