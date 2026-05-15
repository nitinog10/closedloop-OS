from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class QueryState(TypedDict, total=False):
    query: str
    citations: list[dict]
    graph_context: dict
    answer: str
    trace: dict


def retrieve(state: QueryState) -> QueryState:
    return state


def expand_graph(state: QueryState) -> QueryState:
    return state


def generate(state: QueryState) -> QueryState:
    return state


def build_query_graph():
    graph = StateGraph(QueryState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("expand_graph", expand_graph)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "expand_graph")
    graph.add_edge("expand_graph", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
