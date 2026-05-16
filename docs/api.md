# API Surface

## Auth
- `POST /api/v1/auth/login`

## Connector Management
- `GET /api/v1/connectors`
- `POST /api/v1/connectors`
- `GET /api/v1/connectors/{provider}/authorize`
- `GET /api/v1/connectors/{provider}/callback`

## Ingestion
- `POST /api/v1/webhooks/slack`
- `POST /api/v1/webhooks/github`
- `POST /api/v1/webhooks/linear`
- `POST /api/v1/webhooks/notion`
- `POST /api/v1/webhooks/zoom`

## Search & Chat
- `POST /api/v1/search/semantic`
- `POST /api/v1/chat/query`
- `POST /api/v1/chat/stream`

## Graph
- `GET /api/v1/graph/neighborhood/{entity_id}`
- `GET /api/v1/graph/unlinked-work`

## Pipeline Operations
- `POST /api/v1/pipeline/reindex`

## Realtime Notifications
- `GET /api/v1/notifications/recent`
- `WS /api/v1/notifications/ws/{organization_id}`
