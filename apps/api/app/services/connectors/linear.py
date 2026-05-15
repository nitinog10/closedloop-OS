from app.schemas.event import CanonicalEventCreate
from app.services.connectors.base import ConnectorAdapter
from app.services.ingestion.scorer import score_event_importance


class LinearConnectorAdapter(ConnectorAdapter):
    source = "linear"

    async def normalize(self, payload: dict, organization_id: str) -> list[CanonicalEventCreate]:
        data = payload.get("data", payload)
        title = data.get("title") or data.get("identifier") or "Linear issue"
        content = data.get("description") or data.get("comment", {}).get("body") or ""
        identifier = data.get("identifier") or data.get("id") or payload.get("action", "linear")

        return [
            CanonicalEventCreate(
                organization_id=organization_id,
                source="linear",
                source_event_id=str(identifier),
                source_url=data.get("url"),
                event_type=payload.get("type", "issue"),
                actor_external_id=(payload.get("actor") or {}).get("id"),
                channel_external_id=(data.get("team") or {}).get("key"),
                title=title,
                content=content,
                metadata={"raw": payload},
                importance_score=score_event_importance(source="linear", event_type="issue", content=content),
                dedupe_key=f"linear:{identifier}:{payload.get('action', 'event')}",
            )
        ]
