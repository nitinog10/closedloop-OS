from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    type: str
    label: str
    attributes: dict = {}


class GraphEdge(BaseModel):
    source: str
    target: str
    type: str


class GraphNeighborhoodResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
