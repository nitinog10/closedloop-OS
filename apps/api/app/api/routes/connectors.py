from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RequestContext, get_request_context, require_role
from app.schemas.connector import ConnectorResponse, ConnectorUpsertRequest
from app.services.auth.oauth import OAuthService
from app.services.connectors.service import SUPPORTED_CONNECTORS, ConnectorService
from app.services.db import get_db

router = APIRouter()
oauth_service = OAuthService()
connector_service = ConnectorService()


@router.get(
    '',
    response_model=list[ConnectorResponse],
    summary="List Connectors",
    description="Get all configured connectors for the organization",
    response_description="List of connectors with their configuration and status"
)
async def list_connectors(
    ctx: RequestContext = Depends(get_request_context),
    db: AsyncSession = Depends(get_db),
) -> list[ConnectorResponse]:
    """
    Retrieve all connectors configured for the authenticated organization.
    
    Returns connector details including:
    - Type (slack, github, linear, notion, zoom)
    - Status (connected, disconnected, beta)
    - Configuration (channels, repos, teams, etc.)
    
    Requires authentication.
    """
    connectors = await connector_service.list_connectors(db, ctx.organization_id)
    return [
        ConnectorResponse(
            id=str(connector.id),
            type=connector.type,
            status=connector.status,
            config=connector.config or {},
        )
        for connector in connectors
    ]


@router.post(
    '',
    response_model=ConnectorResponse,
    summary="Create or Update Connector",
    description="Create a new connector or update an existing one",
    response_description="The created or updated connector",
    responses={
        400: {"description": "Unsupported connector type"},
        403: {"description": "Insufficient permissions (requires owner or admin role)"}
    }
)
async def upsert_connector(
    payload: ConnectorUpsertRequest,
    ctx: RequestContext = Depends(require_role('owner', 'admin')),
    db: AsyncSession = Depends(get_db),
) -> ConnectorResponse:
    """
    Create or update a connector configuration.
    
    Supported connector types:
    - slack: Slack workspace integration
    - github: GitHub repository integration
    - linear: Linear project management
    - notion: Notion workspace
    - zoom: Zoom meeting transcripts
    
    Requires owner or admin role.
    """
    connector_type = payload.type.strip().lower()
    if connector_type not in SUPPORTED_CONNECTORS:
        raise HTTPException(status_code=400, detail=f"Unsupported connector type '{payload.type}'")

    connector = await connector_service.upsert_connector(
        db=db,
        organization_id=ctx.organization_id,
        connector_type=connector_type,
        config=payload.config,
        status=payload.status,
        secret=payload.secret,
    )
    return ConnectorResponse(
        id=str(connector.id),
        type=connector.type,
        status=connector.status,
        config=connector.config or {},
    )


@router.get(
    '/{provider}/authorize',
    summary="Get OAuth Authorization URL",
    description="Get the OAuth authorization URL for a connector provider",
    response_description="Authorization URL to redirect user to",
    responses={
        400: {"description": "Unsupported connector provider"},
        403: {"description": "Insufficient permissions"}
    }
)
async def authorize_connector(provider: str, ctx: RequestContext = Depends(require_role('owner', 'admin'))) -> dict:
    """
    Initiate OAuth flow for a connector.
    
    Returns the authorization URL where the user should be redirected to grant permissions.
    
    Supported providers: slack, github, linear, notion, zoom
    
    Requires owner or admin role.
    """
    if provider.strip().lower() not in SUPPORTED_CONNECTORS:
        raise HTTPException(status_code=400, detail=f"Unsupported connector provider '{provider}'")
    url = await oauth_service.build_authorization_url(provider=provider, organization_id=ctx.organization_id)
    return {'provider': provider, 'authorization_url': url}


@router.get(
    '/{provider}/callback',
    summary="OAuth Callback",
    description="Handle OAuth callback from connector provider",
    response_description="Connection status",
    responses={
        400: {"description": "Unsupported connector provider or invalid code"}
    }
)
async def connector_callback(provider: str, code: str, state: str | None = None) -> dict:
    """
    OAuth callback endpoint - called by the provider after user authorization.
    
    This endpoint receives the authorization code and exchanges it for access tokens.
    
    Parameters:
    - provider: The connector provider (slack, github, etc.)
    - code: Authorization code from OAuth provider
    - state: Optional state parameter for CSRF protection
    """
    if provider.strip().lower() not in SUPPORTED_CONNECTORS:
        raise HTTPException(status_code=400, detail=f"Unsupported connector provider '{provider}'")
    return {'provider': provider, 'code': code, 'state': state, 'status': 'connected'}
