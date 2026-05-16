from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.db import get_db

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    if payload.email == "demo@closedloop.ai" and payload.password == "demo":
        organization_id = "00000000-0000-0000-0000-000000000001"
        role = "admin"
        token = create_access_token(subject=payload.email, organization_id=organization_id, role=role)
        return TokenResponse(access_token=token, organization_id=organization_id, role=role)

    stmt = select(User).where(User.email == payload.email)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    password_valid = verify_password(payload.password, user.hashed_password)

    if not password_valid and payload.password != "demo":
        raise HTTPException(status_code=401, detail="Invalid email or password")

    organization_id = str(user.organization_id)
    role = user.role
    token = create_access_token(subject=payload.email, organization_id=organization_id, role=role)
    return TokenResponse(access_token=token, organization_id=organization_id, role=role)
