from app.schemas.event import CanonicalEventCreate
from app.services.connectors.base import ConnectorAdapter
from app.services.ingestion.scorer import score_event_importance


class GitHubConnectorAdapter(ConnectorAdapter):
    source = "github"

    async def normalize(self, payload: dict, organization_id: str) -> list[CanonicalEventCreate]:
        action = payload.get("action", "unknown")
        repo = payload.get("repository", {}).get("full_name", "unknown")
        issue = payload.get("issue") or payload.get("pull_request") or {}
        title = issue.get("title") or f"GitHub {action} in {repo}"
        body = issue.get("body") or payload.get("comment", {}).get("body") or ""
        source_url = issue.get("html_url") or payload.get("comment", {}).get("html_url")
        source_event_id = str(issue.get("id") or payload.get("comment", {}).get("id") or payload.get("delivery_id", repo + action))
        event_type = "pull_request" if payload.get("pull_request") else "issue"

        canonical = CanonicalEventCreate(
            organization_id=organization_id,
            source="github",
            source_event_id=source_event_id,
            source_url=source_url,
            event_type=event_type,
            actor_external_id=(payload.get("sender") or {}).get("login"),
            channel_external_id=repo,
            title=title,
            content=body,
            metadata={"raw": payload, "action": action, "repository": repo},
            importance_score=score_event_importance(source="github", event_type=event_type, content=body),
            dedupe_key=f"github:{source_event_id}:{action}",
        )
        return [canonical]
