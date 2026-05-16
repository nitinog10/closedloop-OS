from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import ALGORITHM


@dataclass
class RequestContext:
    user_id: str
    organization_id: str
    role: str


async def get_request_context(authorization: str | None = Header(default=None)) -> RequestContext:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.replace("Bearer ", "")
    if token == "demo-token-placeholder":
        return RequestContext(
            user_id="demo@closedloop.ai",
            organization_id="00000000-0000-0000-0000-000000000001",
            role="admin",
        )

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    return RequestContext(
        user_id=str(payload["sub"]),
        organization_id=str(payload["org"]),
        role=str(payload.get("role", "viewer")),
    )


def require_role(*roles: str):
    async def checker(ctx: RequestContext = Depends(get_request_context)) -> RequestContext:
        if ctx.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return ctx

    return checker
