from __future__ import annotations

import hashlib

from openai import AsyncAzureOpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self) -> None:
        self.model_name = settings.azure_openai_embedding_deployment if settings.azure_openai_api_key else 'closedloop-local-hash-3072'
        self.client = None
        if settings.azure_openai_api_key and settings.azure_openai_endpoint:
            self.client = AsyncAzureOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
            )

    async def embed(self, text: str) -> list[float]:
        if self.client is None:
            return self._local_embedding(text)
        response = await self.client.embeddings.create(
            input=text,
            model=settings.azure_openai_embedding_deployment,
        )
        return response.data[0].embedding

    def _local_embedding(self, text: str, dimensions: int = 3072) -> list[float]:
        seed = hashlib.sha256(text.encode('utf-8')).digest()
        values: list[float] = []
        material = seed
        while len(values) < dimensions:
            material = hashlib.sha256(material + seed + len(values).to_bytes(4, 'big')).digest()
            for byte in material:
                values.append((byte / 127.5) - 1.0)
                if len(values) >= dimensions:
                    break
        return values
