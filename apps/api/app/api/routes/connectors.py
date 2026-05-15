from fastapi import APIRouter, Depends

from app.core.dependencies import RequestContext, get_request_context, require_role
from app.schemas.connector import ConnectorResponse, ConnectorUpsertRequest
from app.services.auth.oauth import OAuthService

router = APIRouter()
oauth_service = OAuthService()


@router.get('', response_model=list[ConnectorResponse])
async def list_connectors(ctx: RequestContext = Depends(get_request_context)) -> list[ConnectorResponse]:
    return [
        ConnectorResponse(id='slack-1', type='slack', status='connected', config={'channels': ['engineering', 'security']}),
        ConnectorResponse(id='github-1', type='github', status='connected', config={'repos': ['closedloop/core']}),
        ConnectorResponse(id='linear-1', type='linear', status='beta', config={'teams': ['PLAT', 'OPS']}),
        ConnectorResponse(id='notion-1', type='notion', status='beta', config={'spaces': ['engineering', 'exec']}),
        ConnectorResponse(id='zoom-1', type='zoom', status='beta', config={'transcripts': True}),
    ]


@router.post('', response_model=ConnectorResponse)
async def upsert_connector(
    payload: ConnectorUpsertRequest,
    _: RequestContext = Depends(require_role('owner', 'admin')),
) -> ConnectorResponse:
    return ConnectorResponse(id=f'{payload.type}-new', type=payload.type, status='connected', config=payload.config)


@router.get('/{provider}/authorize')
async def authorize_connector(provider: str, ctx: RequestContext = Depends(require_role('owner', 'admin'))) -> dict:
    url = await oauth_service.build_authorization_url(provider=provider, organization_id=ctx.organization_id)
    return {'provider': provider, 'authorization_url': url}


@router.get('/{provider}/callback')
async def connector_callback(provider: str, code: str, state: str | None = None) -> dict:
    return {'provider': provider, 'code': code, 'state': state, 'status': 'connected'}
