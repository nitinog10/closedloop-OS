from app.schemas.event import CanonicalEventCreate
from app.services.connectors.base import ConnectorAdapter
from app.services.ingestion.scorer import score_event_importance


class ZoomConnectorAdapter(ConnectorAdapter):
    source = "zoom"

    async def normalize(self, payload: dict, organization_id: str) -> list[CanonicalEventCreate]:
        recording = payload.get("recording") or payload.get("object") or payload
        transcript = recording.get("transcript") or payload.get("transcript") or ""
        meeting_id = recording.get("id") or payload.get("event_ts") or "zoom"
        topic = recording.get("topic") or "Zoom meeting transcript"

        return [
            CanonicalEventCreate(
                organization_id=organization_id,
                source="zoom",
                source_event_id=str(meeting_id),
                source_url=recording.get("share_url"),
                event_type="meeting_transcript",
                actor_external_id=(payload.get("host") or {}).get("id"),
                channel_external_id=recording.get("uuid"),
                title=topic,
                content=transcript,
                metadata={"raw": payload},
                importance_score=score_event_importance(source="zoom", event_type="meeting_transcript", content=transcript),
                dedupe_key=f"zoom:{meeting_id}",
            )
        ]
