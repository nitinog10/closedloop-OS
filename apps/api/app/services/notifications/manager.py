from __future__ import annotations

import json
from collections import defaultdict

from fastapi import WebSocket


class NotificationManager:
    def __init__(self) -> None:
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)
        self.recent_events: dict[str, list[dict]] = defaultdict(list)

    async def connect(self, organization_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[organization_id].add(websocket)

    def disconnect(self, organization_id: str, websocket: WebSocket) -> None:
        if websocket in self.connections.get(organization_id, set()):
            self.connections[organization_id].remove(websocket)

    async def broadcast(self, organization_id: str, payload: dict) -> None:
        recent = self.recent_events[organization_id]
        recent.insert(0, payload)
        del recent[25:]

        dead: list[WebSocket] = []
        for websocket in self.connections.get(organization_id, set()):
            try:
                await websocket.send_text(json.dumps(payload))
            except Exception:
                dead.append(websocket)

        for websocket in dead:
            self.disconnect(organization_id, websocket)

    def list_recent(self, organization_id: str) -> list[dict]:
        return self.recent_events.get(organization_id, [])


notification_manager = NotificationManager()
