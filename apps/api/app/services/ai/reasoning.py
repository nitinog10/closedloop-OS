from __future__ import annotations

from openai import AsyncAzureOpenAI

from app.core.config import settings
from app.schemas.chat import CitationPayload


SYSTEM_PROMPT = """
You are ClosedLoop OS, an enterprise reasoning system.
Answer using only retrieved evidence.
When evidence is incomplete, say so explicitly.
Return concise executive-ready answers with bullet points when useful.
""".strip()


class ReasoningService:
    def __init__(self) -> None:
        self.client = None
        if settings.azure_openai_api_key and settings.azure_openai_endpoint:
            self.client = AsyncAzureOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
            )

    async def answer(self, query: str, citations: list[CitationPayload]) -> tuple[str, dict]:
        evidence = "\n\n".join(
            [f"[{idx+1}] {c.source_title}\n{c.quote}" for idx, c in enumerate(citations)]
        )
        trace = {
            'query': query,
            'evidence_count': len(citations),
            'workflow': ['retrieve', 'rank', 'generate'],
        }

        if self.client is None:
            summary_lines = [
                'ClosedLoop OS provisional answer:',
                f'- Query: {query}',
                f'- Evidence analyzed: {len(citations)} sources',
            ]
            for idx, citation in enumerate(citations[:4], start=1):
                summary_lines.append(f'- [{idx}] {citation.source_title}: {citation.quote[:160]}')
            if not citations:
                summary_lines.append('- No evidence matched strongly enough. Run tenant reindexing or ingest more events.')
            return '\n'.join(summary_lines), trace

        response = await self.client.chat.completions.create(
            model=settings.azure_openai_chat_deployment,
            temperature=0.1,
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {
                    'role': 'user',
                    'content': f'Question: {query}\n\nEvidence:\n{evidence}\n\nUse bracket citations like [1], [2].',
                },
            ],
        )
        content = response.choices[0].message.content or 'No answer generated.'
        return content, trace
