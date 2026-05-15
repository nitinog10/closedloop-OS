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
    docs_url='/docs',
    redoc_url='/redoc',
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
