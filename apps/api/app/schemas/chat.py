from pydantic import BaseModel, Field


class CitationPayload(BaseModel):
    event_id: str
    source_type: str
    source_title: str
    source_url: str | None = None
    quote: str
    relevance_score: float


class ChatQueryRequest(BaseModel):
    query: str = Field(min_length=2)
    conversation_id: str | None = None
    limit: int = 8


class ChatAnswerResponse(BaseModel):
    answer: str
    citations: list[CitationPayload]
    trace: dict
