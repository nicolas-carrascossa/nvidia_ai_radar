"""
Execução ponta a ponta do pipeline de recomendação NVIDIA.

Busca uma startup no Supabase, monta o estado inicial e invoca o grafo LangGraph
completo (classifier → evidence_validator → gap_analyzer → rag_node → briefing).
"""

import logging
import sys

from supabase import create_client

from agents.graph import build_graph
from agents.state import AgentState
from config.settings import settings

logger = logging.getLogger(__name__)

_TABLE = "startups"
_VALID_STATUSES = ("enriquecida", "parcial")


def run_pipeline(startup_nome: str) -> AgentState:
    client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    result = (
        client.table(_TABLE)
        .select("*")
        .eq("nome", startup_nome)
        .in_("status", list(_VALID_STATUSES))
        .limit(1)
        .execute()
    )

    if not result.data:
        raise ValueError(
            f"Startup '{startup_nome}' não encontrada com status "
            f"{_VALID_STATUSES}. Verifique o nome ou o status no banco."
        )

    row = result.data[0]
    logger.info("Startup carregada: %s (status: %s)", row["nome"], row.get("status"))

    initial_state: AgentState = {
        "startup_data": row,
        "retry_count": 0,
    }

    graph = build_graph()
    final_state: AgentState = graph.invoke(initial_state)
    return final_state


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    STARTUP_NOME = "Eva"  # troque aqui para rodar em outra startup

    try:
        state = run_pipeline(STARTUP_NOME)
    except ValueError as e:
        print(f"\nErro: {e}")
        sys.exit(1)

    sep = "=" * 70

    # 1. classificação
    print(f"\n{sep}")
    print("1. CLASSIFICAÇÃO")
    print(sep)
    print(f"  classification : {state.get('classification')}")
    print(f"  confidence     : {state.get('classification_confidence'):.2f}")
    print(f"  reasoning      : {state.get('classification_reasoning')}")

    # 2. veredito do validador
    print(f"\n{sep}")
    print("2. EVIDENCE VALIDATOR")
    print(sep)
    print(f"  verdict        : {state.get('evidence_validator_verdict')}")
    print(f"  retry_count    : {state.get('retry_count')}")

    # 3. gaps (sem item [contexto])
    print(f"\n{sep}")
    print("3. GAPS IDENTIFICADOS")
    print(sep)
    gaps = [g for g in (state.get("gaps_identified") or []) if g.get("tag") != "contexto_geral"]
    for g in gaps:
        print(f"  - {g.get('tag')}: {g.get('evidencia')}")

    # 4. nvidia_context
    print(f"\n{sep}")
    print("4. NVIDIA CONTEXT (chunks RAG)")
    print(sep)
    for i, c in enumerate(state.get("nvidia_context") or [], 1):
        print(f"  [{i}] score={c.get('score', 0):.4f}  tec={c.get('tecnologia')}  fonte={c.get('fonte')}")

    # 5. recommendations
    print(f"\n{sep}")
    print("5. RECOMMENDATIONS")
    print(sep)
    recs = state.get("recommendations") or []
    if not recs:
        print("  (nenhuma recomendação gerada)")
    for rec in recs:
        print(
            f"  • {rec.get('tecnologia')} | "
            f"prioridade: {rec.get('prioridade')} | "
            f"complexidade: {rec.get('complexidade')}"
        )

    # 6. briefing completo
    print(f"\n{sep}")
    print("6. BRIEFING MARKDOWN")
    print(sep)
    print(state.get("briefing") or "(vazio)")

    # 7. errors
    errors = state.get("errors") or []
    if errors:
        print(f"\n{sep}")
        print("7. ERRORS REGISTRADOS")
        print(sep)
        for err in errors:
            print(f"  ! {err}")

    print()
