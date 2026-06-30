"""
Nó 'rag_node' do grafo LangGraph.

Responsabilidade: traduzir os gaps identificados pelo gap_analyzer em uma query de busca
e consultar a base de conhecimento NVIDIA (Qdrant + BM25 + Cohere rerank) para recuperar
chunks relevantes, preenchendo nvidia_context no state.

Reusa diretamente responder() e carregar_corpus_bm25() de rag/scripts/06_generate.py,
carregados via importlib (necessário porque o nome do arquivo começa com dígito).

Estratégia de query: os gaps reais (itens sem prefixo "[contexto]") são concatenados
em uma única string de consulta. Isso permite reutilizar responder() sem modificá-la
e produz uma query coerente com os múltiplos ângulos técnicos da startup. Alternativa
de múltiplas buscas por gap foi descartada por custo de API (N chamadas de rerank).
"""

import importlib.util
import logging
from pathlib import Path

import cohere
from openai import OpenAI
from qdrant_client import QdrantClient

from agents.state import AgentState
from config.settings import settings

logger = logging.getLogger(__name__)

# ── carrega 06_generate.py via importlib ─────────────────────────────────────
# O módulo tem side-effects inofensivos no topo (sys.path, load_dotenv), e já
# carrega internamente 05_hybrid_rerank.py — então carregar_corpus_bm25 também
# fica disponível no namespace do módulo após exec_module.
_RAG_SCRIPTS = Path(__file__).resolve().parents[2] / "rag" / "scripts"

_spec06 = importlib.util.spec_from_file_location(
    "rag_generate", _RAG_SCRIPTS / "06_generate.py"
)
_mod06 = importlib.util.module_from_spec(_spec06)
_spec06.loader.exec_module(_mod06)  # type: ignore[union-attr]

responder = _mod06.responder
carregar_corpus_bm25 = _mod06.carregar_corpus_bm25

def _build_query(gaps_identified: list[dict]) -> str:
    """Join gap evidencias into a single coherent search query.

    Items with tag 'contexto_geral' are reasoning metadata and must be excluded
    from the search — they describe inference context, not actual technical gaps.
    """
    gaps_reais = [g for g in gaps_identified if g.get("tag") != "contexto_geral"]
    if not gaps_reais:
        # fallback: use evidencia from all items (including contexto_geral)
        gaps_reais = gaps_identified
    return ". ".join(g.get("evidencia", "") for g in gaps_reais)


def _to_nvidia_context(chunks: list[dict]) -> list[dict]:
    """Map rerank() output keys to the nvidia_context schema.

    rerank() returns dicts with keys: texto, url, tecnologia, titulo,
    relevance_score (Cohere), plus score_vetorial/score_bm25/fonte from
    the hybrid merge step. We keep only what the briefing node needs.
    """
    return [
        {
            "texto": c.get("texto", ""),
            "fonte": c.get("url", ""),
            "score": float(c.get("relevance_score", 0.0)),
            "tecnologia": c.get("tecnologia", ""),
        }
        for c in chunks
    ]


def query_nvidia_rag(state: AgentState) -> AgentState:
    """LangGraph node: retrieve NVIDIA context for the identified gaps."""
    errors: list[str] = list(state.get("errors") or [])
    gaps_identified: list[dict] = state.get("gaps_identified") or []

    query = _build_query(gaps_identified)
    logger.info("rag_node query: %s", query[:120])

    try:
        bm25, metadados = carregar_corpus_bm25()
        co = cohere.Client(api_key=settings.cohere_api_key)
        qdrant = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        oai = OpenAI(api_key=settings.openai_api_key)
    except Exception as e:
        msg = f"rag_node: falha ao inicializar clients — {e}"
        logger.error(msg)
        errors.append(msg)
        return {**state, "nvidia_context": [], "errors": errors}

    try:
        _answer, chunks = responder(query, co, qdrant, oai, bm25, metadados, top_n=5)
    except Exception as e:
        msg = f"rag_node: falha na busca RAG — {e}"
        logger.error(msg)
        errors.append(msg)
        return {**state, "nvidia_context": [], "errors": errors}

    if not chunks:
        msg = "rag_node: nenhum chunk relevante encontrado para os gaps identificados."
        logger.warning(msg)
        errors.append(msg)
        return {**state, "nvidia_context": [], "errors": errors}

    nvidia_context = _to_nvidia_context(chunks)
    return {**state, "nvidia_context": nvidia_context, "errors": errors}


# ── manual test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import logging as _logging

    _logging.basicConfig(level=_logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    # State fake simulando saída do gap_analyzer — 2 gaps reais + 1 item contexto_geral
    fake_state: AgentState = {
        "startup_data": {
            "nome": "AtendIA",
            "descricao": "Plataforma de atendimento automatizado via LLM.",
            "setor": "tecnologia",
            "modelo_negocio": "SaaS B2B",
            "tecnologias_ia": ["GPT-4", "embeddings"],
            "tipo_ia": "NLP / LLM",
            "founders": [],
            "funding": None,
            "clientes_mencionados": [],
            "status": "enriquecida",
        },
        "retry_count": 0,
        "classification": "AI-native",
        "classification_confidence": 0.88,
        "gaps_identified": [
            {
                "tag": "depende_api_externa_atendimento",
                "evidencia": "Dependência exclusiva de API externa de LLM sem camada de otimização própria, gerando custo variável alto e risco de disponibilidade",
            },
            {
                "tag": "governanca_agentes_ia",
                "evidencia": "Ausência de observabilidade e governança sobre as respostas geradas pelo modelo",
            },
            {
                "tag": "contexto_geral",
                "evidencia": "[contexto] Inferências baseadas na dependência explícita de GPT-4 via API mencionada na descrição; startup processa 50k conversas/dia indicando volume significativo para otimização.",
            },
        ],
    }

    result = query_nvidia_rag(fake_state)

    print("\n" + "=" * 60)
    print("nvidia_context retornado:")
    print("=" * 60)

    context = result.get("nvidia_context") or []
    if not context:
        print("  (vazio — verifique errors abaixo)")
    else:
        for i, item in enumerate(context, 1):
            texto_preview = item["texto"][:150].replace("\n", " ")
            if len(item["texto"]) > 150:
                texto_preview += "..."
            print(f"\n[{i}] tecnologia : {item['tecnologia']}")
            print(f"    fonte      : {item['fonte']}")
            print(f"    score      : {item['score']:.4f}")
            print(f"    texto      : {texto_preview}")

    if result.get("errors"):
        print("\nerrors:")
        for err in result["errors"]:
            print(f"  ! {err}")

    print()
