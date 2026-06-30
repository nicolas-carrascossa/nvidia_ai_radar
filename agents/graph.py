"""
Montagem do grafo LangGraph para o pipeline de recomendação NVIDIA.

Fluxo:
    classifier → evidence_validator
        ↓ (condicional)
        ├─ [rebaixado e retry_count < MAX_RETRIES] → retry_classifier → classifier
        └─ [aceito ou retry esgotado]              → gap_analyzer → rag_node → briefing → END
"""

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.nodes.briefing import generate_briefing
from agents.nodes.classifier import classify_startup
from agents.nodes.evidence_validator import validate_evidence
from agents.nodes.gap_analyzer import analyze_gaps
from agents.nodes.rag_node import query_nvidia_rag
from agents.state import AgentState

MAX_RETRIES = 1


def _route_after_validator(state: AgentState) -> str:
    if (
        state.get("evidence_validator_verdict") == "rebaixado"
        and state["retry_count"] < MAX_RETRIES
    ):
        return "retry_classifier"
    return "gap_analyzer"


def build_graph() -> CompiledStateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("classifier", classify_startup)
    graph.add_node("evidence_validator", validate_evidence)
    graph.add_node("gap_analyzer", analyze_gaps)
    graph.add_node("rag_node", query_nvidia_rag)
    graph.add_node("briefing", generate_briefing)

    # incrementa retry_count antes de voltar ao classifier — sem isso o loop seria infinito
    graph.add_node(
        "retry_classifier",
        lambda state: {**state, "retry_count": state["retry_count"] + 1},
    )

    graph.set_entry_point("classifier")
    graph.add_edge("classifier", "evidence_validator")
    graph.add_conditional_edges(
        "evidence_validator",
        _route_after_validator,
        {"retry_classifier": "retry_classifier", "gap_analyzer": "gap_analyzer"},
    )
    graph.add_edge("retry_classifier", "classifier")
    graph.add_edge("gap_analyzer", "rag_node")
    graph.add_edge("rag_node", "briefing")
    graph.add_edge("briefing", END)

    return graph.compile()
