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


@router.post("/query", response_model=ChatAnswerResponse)
async def query(
    payload: ChatQueryRequest,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> ChatAnswerResponse:
    safety_service.validate_query(payload.query)
    citations = await retrieval_service.semantic_search(db, ctx.organization_id, payload.query, limit=payload.limit)
    graph_context = await graph_reasoner.expand(citations)
    answer, trace = await reasoning_service.answer(payload.query, citations)
    trace["graph_context"] = graph_context
    return ChatAnswerResponse(answer=answer, citations=citations, trace=trace)


@router.post("/stream")
async def query_stream(
    payload: ChatQueryRequest,
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    safety_service.validate_query(payload.query)
    citations = await retrieval_service.semantic_search(db, ctx.organization_id, payload.query, limit=payload.limit)
    answer, _ = await reasoning_service.answer(payload.query, citations)
    return StreamingResponse(stream_text(answer), media_type="text/event-stream")
