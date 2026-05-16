from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import encrypt_secret
from app.models.connector import Connector

SUPPORTED_CONNECTORS = {"slack", "github", "linear", "notion", "zoom"}


class ConnectorService:
    async def list_connectors(self, db: AsyncSession, organization_id: str) -> list[Connector]:
        stmt = (
            select(Connector)
            .where(Connector.organization_id == UUID(organization_id))
            .order_by(Connector.created_at.asc())
        )
        return list((await db.execute(stmt)).scalars().all())

    async def upsert_connector(
        self,
        db: AsyncSession,
        organization_id: str,
        connector_type: str,
        config: dict,
        status: str = "connected",
        secret: str | None = None,
    ) -> Connector:
        normalized_type = connector_type.strip().lower()
        stmt = select(Connector).where(
            Connector.organization_id == UUID(organization_id),
            Connector.type == normalized_type,
        )
        connector = (await db.execute(stmt)).scalar_one_or_none()
        if connector is None:
            connector = Connector(
                organization_id=UUID(organization_id),
                type=normalized_type,
                config=config,
                status=status,
                encrypted_secret=encrypt_secret(secret) if secret else None,
            )
            db.add(connector)
        else:
            connector.config = config
            connector.status = status
            if secret is not None:
                connector.encrypted_secret = encrypt_secret(secret)

        await db.commit()
        await db.refresh(connector)
        return connector
