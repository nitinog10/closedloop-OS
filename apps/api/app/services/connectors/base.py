from abc import ABC, abstractmethod

from app.schemas.event import CanonicalEventCreate


class ConnectorAdapter(ABC):
    source: str

    @abstractmethod
    async def normalize(self, payload: dict, organization_id: str) -> list[CanonicalEventCreate]:
        raise NotImplementedError
