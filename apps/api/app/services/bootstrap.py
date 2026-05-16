from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.models.user import User


DEFAULT_ORG_ID = UUID("00000000-0000-0000-0000-000000000001")
DEFAULT_DEMO_USER_ID = UUID("00000000-0000-0000-0000-000000000101")
DEFAULT_DEMO_HASH = "$2b$12$KIXQ4RO0V7iJ8QKQXQdTNO0HTGvM5QJp8avVnM7oW6J4xDgFJ7b2m"


async def ensure_organization(db: AsyncSession, organization_id: str) -> Organization:
    org_uuid = UUID(str(organization_id))
    org = (await db.execute(select(Organization).where(Organization.id == org_uuid))).scalar_one_or_none()
    if org is not None:
        return org

    org = Organization(
        id=org_uuid,
        name="Acme Enterprise",
        slug="acme-enterprise",
        plan="enterprise",
    )
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org


async def ensure_demo_user(db: AsyncSession) -> User:
    await ensure_organization(db, str(DEFAULT_ORG_ID))
    user = (await db.execute(select(User).where(User.email == "demo@closedloop.ai"))).scalar_one_or_none()
    if user is not None:
        return user

    user = User(
        id=DEFAULT_DEMO_USER_ID,
        organization_id=DEFAULT_ORG_ID,
        email="demo@closedloop.ai",
        full_name="Demo User",
        hashed_password=DEFAULT_DEMO_HASH,
        role="admin",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
