from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _register_models() -> None:
    from app.models import (  # noqa: F401
        audit_log,
        canonical_event,
        citation,
        connector,
        conversation,
        decision,
        embedding,
        entity,
        goal,
        identity_alias,
        notification,
        organization,
        relationship,
        ticket,
        user,
    )


_register_models()

engine = create_async_engine(settings.database_url, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
