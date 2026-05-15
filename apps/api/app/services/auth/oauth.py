class OAuthService:
    async def build_authorization_url(self, provider: str, organization_id: str) -> str:
        return f"/oauth/{provider}?org={organization_id}"
