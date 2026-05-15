from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, get_request_context
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse
from app.services.db import get_db
from app.services.notifications.manager import notification_manager

router = APIRouter()


@router.get('/recent', response_model=list[NotificationResponse])
async def recent_notifications(
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> list[NotificationResponse]:
    stmt = (
        select(Notification)
        .where(Notification.organization_id == UUID(ctx.organization_id))
        .order_by(Notification.created_at.desc())
        .limit(20)
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [
        NotificationResponse(
            id=str(row.id),
            type=row.type,
            title=row.title,
            body=row.body,
            severity=row.severity,
            payload=row.payload,
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.websocket('/ws/{organization_id}')
async def notifications_websocket(websocket: WebSocket, organization_id: str) -> None:
    await notification_manager.connect(organization_id, websocket)
    try:
        for item in notification_manager.list_recent(organization_id):
            await websocket.send_json(item)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_manager.disconnect(organization_id, websocket)
