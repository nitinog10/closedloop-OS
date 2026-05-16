from pydantic import BaseModel


class ConnectorResponse(BaseModel):
    id: str
    type: str
    status: str
    config: dict


class ConnectorUpsertRequest(BaseModel):
    type: str
    config: dict = {}
    secret: str | None = None
    status: str = "connected"
