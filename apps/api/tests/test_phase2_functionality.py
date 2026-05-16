import unittest

from app.core.dependencies import get_request_context
from app.services.auth.oauth import OAuthService
from app.services.connectors.linear import LinearConnectorAdapter
from app.services.connectors.notion import NotionConnectorAdapter
from app.services.connectors.zoom import ZoomConnectorAdapter
from app.services.ingestion.normalizer import normalize_event


ORG_ID = "00000000-0000-0000-0000-000000000001"


class Phase2FunctionalityTests(unittest.IsolatedAsyncioTestCase):
    async def test_linear_connector_normalization(self) -> None:
        payload = {
            "type": "Issue",
            "action": "create",
            "actor": {"id": "linear-user-1"},
            "data": {
                "identifier": "AUTH-142",
                "title": "AUTH-142 Unify auth middleware",
                "description": "Goal: complete identity unification before Q4",
                "url": "https://linear.app/acme/issue/AUTH-142",
                "team": {"key": "PLAT"},
            },
        }
        events = await LinearConnectorAdapter().normalize(payload=payload, organization_id=ORG_ID)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].source, "linear")
        self.assertEqual(events[0].source_event_id, "AUTH-142")
        self.assertEqual(events[0].channel_external_id, "PLAT")

    async def test_notion_connector_normalization(self) -> None:
        payload = {
            "type": "document",
            "actor": {"id": "notion-editor"},
            "page": {
                "id": "page-auth-001",
                "title": "Authentication Architecture Decision Record",
                "content": "Decision: centralized token validation",
                "url": "https://notion.so/acme/auth-architecture",
                "space_id": "engineering",
            },
        }
        events = await NotionConnectorAdapter().normalize(payload=payload, organization_id=ORG_ID)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].source, "notion")
        self.assertEqual(events[0].source_event_id, "page-auth-001")
        self.assertEqual(events[0].channel_external_id, "engineering")

    async def test_zoom_connector_normalization(self) -> None:
        payload = {
            "object": {
                "id": "zoom-meeting-1",
                "uuid": "zoom-uuid-1",
                "topic": "Platform auth architecture",
            },
            "host": {"id": "zoom-host-1"},
            "transcript": "Decision: move to centralized auth middleware.",
        }
        events = await ZoomConnectorAdapter().normalize(payload=payload, organization_id=ORG_ID)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].source, "zoom")
        self.assertEqual(events[0].event_type, "meeting_transcript")
        self.assertEqual(events[0].source_event_id, "zoom-meeting-1")

    async def test_normalizer_rejects_unknown_source(self) -> None:
        with self.assertRaises(ValueError):
            await normalize_event("unknown-source", {"a": 1}, ORG_ID)

    async def test_oauth_url_contains_provider_and_org(self) -> None:
        url = await OAuthService().build_authorization_url("github", ORG_ID)
        self.assertIn("/integrations/github/connect?", url)
        self.assertIn("organization_id=00000000-0000-0000-0000-000000000001", url)
        self.assertIn("redirect_uri=", url)

    async def test_demo_placeholder_token_works(self) -> None:
        ctx = await get_request_context("Bearer demo-token-placeholder")
        self.assertEqual(ctx.organization_id, ORG_ID)
        self.assertEqual(ctx.role, "admin")


if __name__ == "__main__":
    unittest.main()
