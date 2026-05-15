from app.schemas.event import CanonicalEventCreate
from app.services.connectors.base import ConnectorAdapter
from app.services.ingestion.scorer import score_event_importance


class SlackConnectorAdapter(ConnectorAdapter):
    source = "slack"

    async def normalize(self, payload: dict, organization_id: str) -> list[CanonicalEventCreate]:
        event = payload.get("event", payload)
        text = event.get("text", "")
        channel = event.get("channel")
        ts = event.get("ts", payload.get("event_id", "unknown"))
        title = f"Slack message in #{channel}" if channel else "Slack message"
        canonical = CanonicalEventCreate(
            organization_id=organization_id,
            source="slack",
            source_event_id=str(payload.get("event_id", ts)),
            source_url=payload.get("source_url"),
            event_type=event.get("type", "message"),
            actor_external_id=event.get("user"),
            channel_external_id=channel,
            title=title,
            content=text,
            metadata={"raw": payload},
            importance_score=score_event_importance(source="slack", event_type=event.get("type", "message"), content=text),
            dedupe_key=f"slack:{payload.get('event_id', ts)}",
        )
        return [canonical]
