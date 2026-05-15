from app.schemas.event import CanonicalEventCreate
from app.services.connectors.base import ConnectorAdapter
from app.services.ingestion.scorer import score_event_importance


class NotionConnectorAdapter(ConnectorAdapter):
    source = "notion"

    async def normalize(self, payload: dict, organization_id: str) -> list[CanonicalEventCreate]:
        page = payload.get("page", payload)
        title = page.get("title") or page.get("name") or "Notion document"
        content = page.get("content") or page.get("summary") or ""
        page_id = page.get("id") or payload.get("event_id", title)

        return [
            CanonicalEventCreate(
                organization_id=organization_id,
                source="notion",
                source_event_id=str(page_id),
                source_url=page.get("url"),
                event_type=payload.get("type", "document"),
                actor_external_id=(payload.get("actor") or {}).get("id"),
                channel_external_id=page.get("space_id"),
                title=title,
                content=content,
                metadata={"raw": payload},
                importance_score=score_event_importance(source="notion", event_type="document", content=content),
                dedupe_key=f"notion:{page_id}",
            )
        ]
