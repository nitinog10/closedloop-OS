from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.services.notifications.manager import notification_manager


class NotificationService:
    async def publish(
        self,
        db: AsyncSession,
        organization_id: str,
        notification_type: str,
        title: str,
        body: str,
        severity: str = 'info',
        payload: dict | None = None,
    ) -> Notification:
        record = Notification(
            organization_id=UUID(organization_id),
            type=notification_type,
            title=title,
            body=body,
            severity=severity,
            payload=payload or {},
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)

        await notification_manager.broadcast(
            organization_id,
            {
                'id': str(record.id),
                'type': record.type,
                'title': record.title,
                'body': record.body,
                'severity': record.severity,
                'payload': record.payload,
                'created_at': record.created_at.isoformat(),
            },
        )
        return record
