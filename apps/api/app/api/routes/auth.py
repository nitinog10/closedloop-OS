from fastapi import APIRouter, HTTPException

from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    if payload.password != "demo":
        raise HTTPException(status_code=401, detail="Use password 'demo' for local scaffold access")

    organization_id = "00000000-0000-0000-0000-000000000001"
    role = "admin"
    token = create_access_token(subject=payload.email, organization_id=organization_id, role=role)
    return TokenResponse(access_token=token, organization_id=organization_id, role=role)
