"""
Motor de recomendação (Fase 4) — módulo independente, ainda sem LangGraph.

Responsabilidade: cruzar os gaps identificados (Fase 3 — gap_analyzer) com o contexto
NVIDIA recuperado pelo RAG (Fase 2 — rag_node) e gerar a lista final de recomendações
de tecnologia, cada uma com justificativa técnica/negócio e próxima ação.

Prioridade e complexidade são calculadas em Python puro (regra de negócio determinística,
sem LLM). O LLM só escreve a prosa (justificativas e próxima ação) — não decide
prioridade nem complexidade, que vêm prontas no prompt.
"""

import json
import logging
import re
import time

from openai import OpenAI

from config.settings import settings

logger = logging.getLogger(__name__)

_MODEL = "gpt-4o-mini"
_RETRY_DELAYS = [5, 10, 20]

GAP_TO_TECH: dict[str, list[str]] = {
    "depende_api_externa_atendimento": ["NIM", "NeMo Guardrails", "Triton"],
    "alto_volume_dados_tabulares": ["RAPIDS", "cuDF", "cuML"],
    "voz_call_center_transcricao": ["Riva", "NIM"],
    "atua_em_saude": ["Clara", "MONAI", "NIM", "NeMo Guardrails", "AI Enterprise"],
    "robotica_ou_simulacao": ["Isaac", "Omniverse", "GPUs NVIDIA"],
    "latencia_de_inferencia": ["Triton", "TensorRT-LLM", "batching"],
    "governanca_agentes_ia": ["NeMo Guardrails", "NeMo"],
    "ausencia_adocao_ia": ["NIM", "NeMo"],
}

TECH_COMPLEXITY: dict[str, list[str]] = {
    "Baixa": ["NIM", "NeMo Guardrails"],
    "Média": ["Triton", "RAPIDS", "cuDF", "cuML", "Riva", "NeMo", "batching"],
    "Alta": ["TensorRT-LLM", "CUDA", "Omniverse", "Clara", "Isaac", "GPUs NVIDIA", "MONAI", "AI Enterprise"],
}

_SYSTEM_PROMPT = """\
Você é um especialista em soluções técnicas NVIDIA que escreve recomendações para o \
time de vendas/solutions da NVIDIA avaliar uma startup.

Você recebe uma lista de tecnologias NVIDIA já selecionadas (com prioridade e \
complexidade já calculadas — não as altere), os gaps técnicos identificados na startup \
e trechos de contexto recuperados da documentação NVIDIA.

Para CADA tecnologia da lista recebida, escreva:
- justificativa_tecnica: por que essa tecnologia resolve o(s) gap(s) técnico(s) da startup, \
com base no contexto NVIDIA fornecido quando disponível.
- justificativa_negocio: o ganho de negócio esperado para a startup (custo, velocidade, \
escala, compliance, etc.), em linguagem acessível a um non-tech.
- proxima_acao: uma ação concreta e curta para o time NVIDIA dar seguimento com essa \
startup (ex: "agendar demo técnica do NIM com o time de engenharia", "enviar whitepaper \
de compliance do Clara").

REGRAS:
- Responda para TODAS as tecnologias da lista recebida, nenhuma de menos, nenhuma extra.
- Use exatamente o nome da tecnologia como recebido (não traduza, não abrevie diferente).
- Seja específico — conecte a justificativa aos gaps e evidências fornecidas, não genérico.

FORMATO DE SAÍDA — responda SOMENTE com um array JSON válido, sem texto antes ou depois, \
sem markdown, sem ```json:
[
  {
    "tecnologia": "<nome exato da tecnologia>",
    "justificativa_tecnica": "<...>",
    "justificativa_negocio": "<...>",
    "proxima_acao": "<...>"
  }
]\
"""


def _strip_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _chat_with_retry(oai: OpenAI, messages: list[dict]) -> str:
    for attempt, delay in enumerate(_RETRY_DELAYS):
        try:
            resp = oai.chat.completions.create(
                model=_MODEL,
                messages=messages,
                temperature=0,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            if attempt == len(_RETRY_DELAYS) - 1:
                raise
            logger.warning(
                "OpenAI attempt %d/%d failed: %s. Retrying in %ds...",
                attempt + 1,
                len(_RETRY_DELAYS),
                e,
                delay,
            )
            time.sleep(delay)
    return ""  # unreachable


def _tech_complexity(tech: str) -> str:
    for complexity, techs in TECH_COMPLEXITY.items():
        if tech in techs:
            return complexity
    return "Média"


def _determine_base_recommendations(gaps: list[dict]) -> dict[str, dict]:
    """Cruza as tags dos gaps com GAP_TO_TECH e calcula prioridade/complexidade por tecnologia.

    Prioridade: >=2 gaps distintos mapeando pra mesma tech => 'Alta'; 1 gap => 'Média';
    senão (não deveria ocorrer aqui, mas por segurança) => 'Baixa'.

    Retorna {tecnologia: {"prioridade": str, "complexidade": str, "gap_count": int}}.
    """
    tech_gap_count: dict[str, int] = {}

    for gap in gaps:
        tag = gap.get("tag")
        if tag == "contexto_geral":
            continue
        for tech in GAP_TO_TECH.get(tag, []):
            tech_gap_count[tech] = tech_gap_count.get(tech, 0) + 1

    base: dict[str, dict] = {}
    for tech, count in tech_gap_count.items():
        if count >= 2:
            prioridade = "Alta"
        elif count == 1:
            prioridade = "Média"
        else:
            prioridade = "Baixa"
        base[tech] = {
            "prioridade": prioridade,
            "complexidade": _tech_complexity(tech),
            "gap_count": count,
        }

    return base


def _build_user_message(
    base_recommendations: dict[str, dict],
    gaps_identified: list[dict],
    nvidia_context: list[dict],
) -> str:
    tech_lines = "\n".join(
        f"  - {tech} (prioridade pré-calculada: {info['prioridade']}, "
        f"complexidade pré-calculada: {info['complexidade']})"
        for tech, info in base_recommendations.items()
    )

    gap_lines = "\n".join(
        f"  - [{g.get('tag')}] {g.get('evidencia')}" for g in gaps_identified
    )

    context_lines = "\n".join(
        f"  - ({c.get('tecnologia', '?')}) {c.get('texto', '')[:400]}"
        for c in nvidia_context
    )

    return (
        "TECNOLOGIAS NVIDIA SELECIONADAS (escreva justificativas para todas, "
        "sem alterar prioridade/complexidade):\n"
        f"{tech_lines or '  (nenhuma)'}\n"
        "\n"
        "GAPS IDENTIFICADOS NA STARTUP:\n"
        f"{gap_lines or '  (nenhum)'}\n"
        "\n"
        "CONTEXTO NVIDIA RECUPERADO (RAG):\n"
        f"{context_lines or '  (nenhum contexto disponível)'}"
    )


def generate_recommendations(
    gaps_identified: list[dict], nvidia_context: list[dict]
) -> list[dict]:
    """Gera a lista final de recomendações NVIDIA para a startup.

    Combina cálculo determinístico (prioridade/complexidade, via _determine_base_recommendations)
    com prosa gerada por LLM (justificativas e próxima ação). Retorna list[dict] compatível
    com o campo `recommendations` do AgentState.
    """
    base_recommendations = _determine_base_recommendations(gaps_identified)

    if not base_recommendations:
        logger.warning("recommendation_engine: nenhuma tecnologia mapeada a partir dos gaps.")
        return []

    oai = OpenAI(api_key=settings.openai_api_key)
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {
            "role": "user",
            "content": _build_user_message(base_recommendations, gaps_identified, nvidia_context),
        },
    ]

    raw = ""
    try:
        raw = _chat_with_retry(oai, messages)
        parsed = json.loads(_strip_fences(raw))
    except json.JSONDecodeError as e:
        logger.error(
            "recommendation_engine: JSON inválido na resposta do LLM — %s. Raw: %s",
            e,
            raw[:200],
        )
        parsed = []
    except Exception as e:
        logger.error("recommendation_engine: erro na chamada OpenAI — %s", e)
        parsed = []

    if not isinstance(parsed, list):
        logger.warning("recommendation_engine: LLM não retornou um array JSON.")
        parsed = []

    recommendations: list[dict] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        tech = item.get("tecnologia")
        info = base_recommendations.get(tech)
        if info is None:
            logger.warning(
                "recommendation_engine: LLM retornou tecnologia fora da lista esperada — '%s'.",
                tech,
            )
            continue
        recommendations.append(
            {
                "tecnologia": tech,
                "justificativa_tecnica": str(item.get("justificativa_tecnica", "")),
                "justificativa_negocio": str(item.get("justificativa_negocio", "")),
                "proxima_acao": str(item.get("proxima_acao", "")),
                "prioridade": info["prioridade"],
                "complexidade": info["complexidade"],
            }
        )

    # Garante que toda tecnologia base apareça, mesmo se o LLM esqueceu alguma.
    covered = {r["tecnologia"] for r in recommendations}
    for tech, info in base_recommendations.items():
        if tech in covered:
            continue
        logger.warning("recommendation_engine: tecnologia '%s' ausente na resposta do LLM — usando fallback.", tech)
        recommendations.append(
            {
                "tecnologia": tech,
                "justificativa_tecnica": "Não foi possível gerar justificativa automaticamente.",
                "justificativa_negocio": "Não foi possível gerar justificativa automaticamente.",
                "proxima_acao": "Revisar manualmente.",
                "prioridade": info["prioridade"],
                "complexidade": info["complexidade"],
            }
        )

    return recommendations
