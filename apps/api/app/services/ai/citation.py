from app.schemas.chat import CitationPayload


class CitationEngine:
    def build_index(self, citations: list[CitationPayload]) -> dict[str, int]:
        return {citation.event_id: index + 1 for index, citation in enumerate(citations)}
