from app.core.dependencies import RequestContext


class AuditService:
    async def record(self, ctx: RequestContext, action: str, resource_type: str, resource_id: str, payload: dict | None = None) -> None:
        return None
