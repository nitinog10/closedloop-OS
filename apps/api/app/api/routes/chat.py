from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, get_request_context
from app.schemas.chat import ChatAnswerResponse, ChatQueryRequest
from app.services.ai.graph_reasoner import GraphReasoner
from app.services.ai.reasoning import ReasoningService
from app.services.ai.retrieval import RetrievalService
from app.services.ai.safety import SafetyService
from app.services.ai.streaming import stream_text
from app.services.db import get_db

router = APIRouter()
retrieval_service = RetrievalService()
reasoning_service = ReasoningService()
graph_reasoner = GraphReasoner()
safety_service = SafetyService()


@router.post(
    "/query",
    response_model=ChatAnswerResponse,
    summary="Query with AI Reasoning",
    description="Ask questions about your organization's data and get AI-powered answers with citations",
    response_description="Answer with citations and reasoning trace"
)
async def query(
    payload: ChatQueryRequest,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> ChatAnswerResponse:
    """
    AI-powered query answering with full reasoning chain.
    
    Workflow:
    1. **Retrieve**: Semantic search for relevant context
    2. **Expand**: Graph traversal to find connected entities
    3. **Reason**: LLM generates answer from evidence
    4. **Cite**: All claims linked to source events
    
    Example queries:
    - "What did we decide about authentication last quarter?"
    - "Why did sprint 47 slip?"
    - "Show me all work not tied to customer requests"
    - "What are the blockers for the Q2 launch?"
    
    Request body:
    ```json
    {
        "query": "What did we decide about pricing?",
        "limit": 8
    }
    ```
    
    Returns:
    - Natural language answer
    - Citations with source links
    - Reasoning trace (retrieval → graph → generation)
    - Graph context (connected entities)
    
    Requires authentication.
    """
    safety_service.validate_query(payload.query)
    citations = await retrieval_service.semantic_search(db, ctx.organization_id, payload.query, limit=payload.limit)
    graph_context = await graph_reasoner.expand(citations)
    answer, trace = await reasoning_service.answer(payload.query, citations)
    trace["graph_context"] = graph_context
    return ChatAnswerResponse(answer=answer, citations=citations, trace=trace)


@router.post(
    "/stream",
    summary="Query with Streaming Response",
    description="Same as /query but streams the answer token-by-token for real-time UX",
    response_description="Server-sent events stream of answer tokens",
    responses={
        200: {
            "description": "Streaming response",
            "content": {"text/event-stream": {"example": "data: What\ndata: did\ndata: we\n..."}}
        }
    }
)
async def query_stream(
    payload: ChatQueryRequest,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """
    Streaming version of the query endpoint.
    
    Returns answer as server-sent events for real-time display.
    
    Useful for chat interfaces where you want to show the answer
    as it's being generated rather than waiting for completion.
    
    Response format: text/event-stream
    ```
    data: What
    data: did
    data: we
    data: decide
    ...
    ```
    
    Requires authentication.
    """
    safety_service.validate_query(payload.query)
    citations = await retrieval_service.semantic_search(db, ctx.organization_id, payload.query, limit=payload.limit)
    answer, _ = await reasoning_service.answer(payload.query, citations)
    return StreamingResponse(stream_text(answer), media_type="text/event-stream")
