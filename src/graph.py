from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from nodes import (
    intake_node,
    supervisor_node,
    company_info_node,
    regulatory_node,
    financing_node,
    aggregate_score_node,
    human_approval_node,
    recommendation_node,
)
from nodes.intake import MAState


def build_graph():
    builder = StateGraph(MAState)

    # Узлы
    builder.add_node("intake", intake_node)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("company_info", company_info_node)
    builder.add_node("regulatory", regulatory_node)
    builder.add_node("financing", financing_node)
    builder.add_node("aggregate_score", aggregate_score_node)
    builder.add_node("human_approval", human_approval_node)
    builder.add_node("recommendation", recommendation_node)

    # Рёбра
    builder.add_edge(START, "intake")
    builder.add_edge("intake", "supervisor")

    # “worker → supervisor” цикл
    for w in ["company_info", "regulatory", "financing", "aggregate_score", "human_approval"]:
        builder.add_edge(w, "supervisor")

    builder.add_edge("supervisor", "recommendation")
    builder.add_edge("recommendation", END)

    checkpointer = InMemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    return graph


graph = build_graph()
