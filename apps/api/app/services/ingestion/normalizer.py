from app.schemas.event import CanonicalEventCreate
from app.services.connectors.github import GitHubConnectorAdapter
from app.services.connectors.linear import LinearConnectorAdapter
from app.services.connectors.notion import NotionConnectorAdapter
from app.services.connectors.slack import SlackConnectorAdapter
from app.services.connectors.zoom import ZoomConnectorAdapter

ADAPTERS = {
    'slack': SlackConnectorAdapter(),
    'github': GitHubConnectorAdapter(),
    'linear': LinearConnectorAdapter(),
    'notion': NotionConnectorAdapter(),
    'zoom': ZoomConnectorAdapter(),
}


async def normalize_event(source: str, payload: dict, organization_id: str) -> list[CanonicalEventCreate]:
    adapter = ADAPTERS[source]
    return await adapter.normalize(payload=payload, organization_id=organization_id)
