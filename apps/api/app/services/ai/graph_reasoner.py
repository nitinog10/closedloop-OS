from app.schemas.chat import CitationPayload


class GraphReasoner:
    async def expand(self, citations: list[CitationPayload]) -> dict:
        return {
            "expanded_entities": [],
            "decision_threads": [citation.source_title for citation in citations[:3]],
        }
