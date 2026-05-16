from urllib.parse import urlencode

from app.core.config import settings


class OAuthService:
    async def build_authorization_url(self, provider: str, organization_id: str) -> str:
        callback_url = f"{settings.api_url.rstrip('/')}/api/v1/connectors/{provider}/callback"
        query = urlencode({"organization_id": organization_id, "redirect_uri": callback_url})
        return f"{settings.app_url.rstrip('/')}/integrations/{provider}/connect?{query}"
