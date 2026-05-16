from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, chat, connectors, events, graph, health, notifications, pipeline, search
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import InMemoryRateLimitMiddleware

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version='0.2.0',
    description="""
## ClosedLoop OS API

The Intelligence Layer That Makes Companies Queryable

### Core Capabilities

**Universal Connector Framework**
- Real-time ingestion from Slack, Linear, GitHub, Notion, Zoom
- Webhook-first architecture with OAuth2 authentication
- Automatic event normalization and deduplication

**Unified Event Stream & Knowledge Store**
- Canonical event schema across all tools
- Vector embeddings for semantic search
- Temporal event tracking and replay

**Semantic Company Graph**
- Entity resolution (People, Teams, Projects, Goals, Decisions)
- Relationship mapping (authored, decided, blocked_by, depends_on)
- Graph traversal and path queries

**Reasoning Engine**
- AI-powered query answering with citations
- Goal tracking and alignment checking
- Anomaly detection (unlinked work, missing context)
- Decision tracing and causal analysis

**Action Layer**
- Generate and assign tickets
- Draft messages and documents
- Human-in-the-loop approval flows
- Full audit trail

### Authentication

Most endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Organization Context

Multi-tenant architecture - all requests are scoped to an organization via:
- JWT token (contains organization_id)
- Or X-Organization-Id header for webhook endpoints

### Rate Limiting

API is rate-limited to 120 requests per minute per IP address.

### Webhooks

Webhook endpoints (`/api/v1/webhooks/*`) accept events from external tools:
- Slack: `/api/v1/webhooks/slack`
- GitHub: `/api/v1/webhooks/github`
- Linear: `/api/v1/webhooks/linear`
- Notion: `/api/v1/webhooks/notion`
- Zoom: `/api/v1/webhooks/zoom`

### Real-time Updates

WebSocket endpoint for real-time notifications:
```
ws://localhost:8000/api/v1/notifications/ws/{organization_id}
```
    """,
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and system status endpoints"
        },
        {
            "name": "auth",
            "description": "Authentication and authorization endpoints"
        },
        {
            "name": "connectors",
            "description": "Connector management - OAuth flows, configuration, and status"
        },
        {
            "name": "events",
            "description": "Webhook endpoints for ingesting events from external tools"
        },
        {
            "name": "search",
            "description": "Semantic search across all organizational data"
        },
        {
            "name": "graph",
            "description": "Knowledge graph queries - entities, relationships, and traversal"
        },
        {
            "name": "chat",
            "description": "AI-powered reasoning and query answering with citations"
        },
        {
            "name": "notifications",
            "description": "Real-time notifications and alerts"
        },
        {
            "name": "pipeline",
            "description": "Data pipeline management - reindexing and processing"
        }
    ],
    contact={
        "name": "ClosedLoop OS",
        "url": "https://closedloop.ai",
        "email": "support@closedloop.ai"
    },
    license_info={
        "name": "Proprietary",
    }
)

app.add_middleware(InMemoryRateLimitMiddleware, requests_per_minute=120)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router)
app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(connectors.router, prefix='/api/v1/connectors', tags=['connectors'])
app.include_router(events.router, prefix='/api/v1/webhooks', tags=['events'])
app.include_router(search.router, prefix='/api/v1/search', tags=['search'])
app.include_router(graph.router, prefix='/api/v1/graph', tags=['graph'])
app.include_router(chat.router, prefix='/api/v1/chat', tags=['chat'])
app.include_router(notifications.router, prefix='/api/v1/notifications', tags=['notifications'])
app.include_router(pipeline.router, prefix='/api/v1/pipeline', tags=['pipeline'])


@app.get('/')
async def root() -> dict[str, str]:
    return {'name': settings.app_name, 'status': 'ok'}
