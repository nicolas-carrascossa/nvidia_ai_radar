"""
Nó 'briefing' do grafo LangGraph — nó terminal.

Responsabilidade: consolidar todo o contexto acumulado no state (classificação,
evidências, gaps, chunks RAG) e produzir dois artefatos finais:
  - recommendations: lista de tecnologias NVIDIA recomendadas, calculada pelo
    recommendation_engine (Fase 4) — este nó NÃO gera recomendações do zero.
  - briefing: relatório executivo em markdown para o time NVIDIA Inception, que
    espelha fielmente as recommendations já calculadas.
"""

import json
import logging
import re
import time

from openai import OpenAI

from agents.recommendation_engine import generate_recommendations
from agents.state import AgentState
from config.settings import settings

logger = logging.getLogger(__name__)

_MODEL = "gpt-4o-mini"
_RETRY_DELAYS = [5, 10, 20]

_LOW_SCORE_THRESHOLD = 0.3

_SYSTEM_PROMPT = """\
Você é um consultor técnico sênior especializado em tecnologias NVIDIA, produzindo \
relatórios executivos para o programa NVIDIA Inception sobre startups brasileiras de IA.

Sua tarefa é gerar APENAS o relatório em markdown (briefing). A lista de tecnologias \
recomendadas (recommendations) já foi calculada por um motor de regras de negócio e \
está incluída nos dados fornecidos — você não decide quais tecnologias recomendar, \
você apenas relata o que já foi decidido.

REGRA DE FIDELIDADE (terminante):
- Espelhe fielmente, na seção "Tecnologias Recomendadas" do briefing, EXATAMENTE as \
tecnologias da lista recommendations fornecida — para cada uma, reproduza tecnologia, \
justificativa_tecnica, justificativa_negocio, prioridade, complexidade e proxima_acao.
- É TERMINANTEMENTE PROIBIDO inventar, adicionar, remover ou substituir qualquer \
tecnologia que não esteja na lista recommendations fornecida.
- Não altere os valores de prioridade ou complexidade fornecidos.

SOBRE O BRIEFING:
- Use linguagem executiva mas precisa tecnicamente.
- Seções obrigatórias: Classificação, Gaps Identificados, Tecnologias Recomendadas, \
Justificativas, Próximas Ações.
- Inclua a seção "Limitações e Ressalvas" se errors não estiver vazio OU se todos os \
chunks do contexto RAG tiverem score < 0.3 (baixa cobertura na base de conhecimento).
- Não inclua dados que não estejam no contexto fornecido.

FORMATO DE SAÍDA — responda SOMENTE com um objeto JSON válido, sem texto antes ou depois, \
sem markdown, sem ```json:
{
  "briefing_md": "<relatório completo em markdown com as seções obrigatórias>"
}\
"""


def _format_startup_data(sd: dict) -> str:
    founders = sd.get("founders") or []
    clientes = sd.get("clientes_mencionados") or []
    tecnologias = sd.get("tecnologias_ia") or []
    return (
        f"  nome: {sd.get('nome') or '(não informado)'}\n"
        f"  site: {sd.get('site') or '(não informado)'}\n"
        f"  descricao: {sd.get('descricao') or '(não informado)'}\n"
        f"  setor: {sd.get('setor') or '(não informado)'}\n"
        f"  modelo_negocio: {sd.get('modelo_negocio') or '(não informado)'}\n"
        f"  tecnologias_ia: {', '.join(tecnologias) or '(não informado)'}\n"
        f"  tipo_ia: {sd.get('tipo_ia') or '(não informado)'}\n"
        f"  founders: {', '.join(founders) if founders else '(não informado)'}\n"
        f"  funding: {sd.get('funding') or '(não informado)'}\n"
        f"  clientes_mencionados: {', '.join(clientes) if clientes else '(não informado)'}"
    )


def _format_nvidia_context(nvidia_context: list[dict]) -> tuple[str, bool]:
    """Return (formatted_string, all_scores_low).

    Trunca cada chunk a 300 chars para não estourar o contexto do LLM.
    Retorna também se TODOS os scores são abaixo de _LOW_SCORE_THRESHOLD.
    """
    if not nvidia_context:
        return "(nenhum chunk recuperado)", True

    all_low = all(c.get("score", 0.0) < _LOW_SCORE_THRESHOLD for c in nvidia_context)
    lines = []
    for i, c in enumerate(nvidia_context, 1):
        texto = c.get("texto", "")
        texto_preview = texto[:300] + ("..." if len(texto) > 300 else "")
        score = c.get("score", 0.0)
        low_flag = " [BAIXA RELEVÂNCIA]" if score < _LOW_SCORE_THRESHOLD else ""
        lines.append(
            f"[{i}] tecnologia: {c.get('tecnologia', '?')} | "
            f"score: {score:.3f}{low_flag}\n"
            f"    fonte: {c.get('fonte', '?')}\n"
            f"    trecho: {texto_preview}"
        )
    return "\n\n".join(lines), all_low


def _format_recommendations(recommendations: list[dict]) -> str:
    if not recommendations:
        return "(nenhuma recomendação calculada)"
    lines = []
    for i, r in enumerate(recommendations, 1):
        lines.append(
            f"[{i}] tecnologia: {r.get('tecnologia')}\n"
            f"    prioridade: {r.get('prioridade')} | complexidade: {r.get('complexidade')}\n"
            f"    justificativa_tecnica: {r.get('justificativa_tecnica')}\n"
            f"    justificativa_negocio: {r.get('justificativa_negocio')}\n"
            f"    proxima_acao: {r.get('proxima_acao')}"
        )
    return "\n\n".join(lines)


def _build_user_message(
    state: AgentState, recommendations: list[dict], all_scores_low: bool
) -> str:
    sd = state["startup_data"]
    errors = state.get("errors") or []

    evidence_lines = "\n".join(f"  - {e}" for e in (state.get("evidence") or []))
    gaps_lines = "\n".join(
        f"  - [{g.get('tag')}] {g.get('evidencia')}"
        for g in (state.get("gaps_identified") or [])
    )

    nvidia_ctx_str, _ = _format_nvidia_context(state.get("nvidia_context") or [])
    recommendations_str = _format_recommendations(recommendations)

    cobertura_aviso = (
        "\n⚠ ATENÇÃO: todos os chunks do contexto RAG têm score < 0.3 — cobertura "
        "baixa. Inclua a seção 'Limitações e Ressalvas' no briefing."
        if all_scores_low
        else ""
    )

    errors_block = ""
    if errors:
        errors_lines = "\n".join(f"  - {e}" for e in errors)
        errors_block = (
            f"\nERROS NÃO-FATAIS REGISTRADOS DURANTE O PIPELINE "
            f"(incluir em 'Limitações e Ressalvas'):\n{errors_lines}"
        )

    return (
        "DADOS DA STARTUP:\n"
        f"{_format_startup_data(sd)}\n"
        "\n"
        "CLASSIFICAÇÃO:\n"
        f"  classification: {state.get('classification')}\n"
        f"  confidence: {state.get('classification_confidence')}\n"
        f"  reasoning: {state.get('classification_reasoning') or '(não informado)'}\n"
        "\n"
        "EVIDÊNCIAS E AUDITORIA:\n"
        f"{evidence_lines or '  (nenhuma)'}\n"
        "\n"
        "GAPS IDENTIFICADOS:\n"
        f"{gaps_lines or '  (nenhum)'}\n"
        "\n"
        "RECOMMENDATIONS (já calculadas pelo recommendation_engine — espelhe fielmente, "
        "não invente nem altere):\n"
        f"{recommendations_str}\n"
        "\n"
        f"CONTEXTO RAG (trechos NVIDIA, truncados a 300 chars):{cobertura_aviso}\n"
        f"{nvidia_ctx_str}"
        f"{errors_block}"
    )


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


def generate_briefing(state: AgentState) -> AgentState:
    """LangGraph node: run the recommendation engine and produce the final markdown briefing."""
    errors: list[str] = list(state.get("errors") or [])
    nome = state["startup_data"].get("nome", "startup")

    recommendations = generate_recommendations(
        state.get("gaps_identified", []), state.get("nvidia_context", [])
    )

    nvidia_context = state.get("nvidia_context") or []
    _, all_scores_low = _format_nvidia_context(nvidia_context)

    oai = OpenAI(api_key=settings.openai_api_key)
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_message(state, recommendations, all_scores_low)},
    ]

    raw = ""
    try:
        raw = _chat_with_retry(oai, messages)
        parsed = json.loads(_strip_fences(raw))
    except json.JSONDecodeError as e:
        msg = f"briefing: JSON inválido na resposta do LLM — {e}. Raw: {raw[:200]}"
        logger.error(msg)
        errors.append(msg)
        fallback_md = (
            f"## {nome} — Briefing NVIDIA Inception\n\n"
            "**Erro:** falha ao gerar briefing — resposta do LLM não pôde ser parseada.\n\n"
            f"### Limitações e Ressalvas\n- {msg}"
        )
        return {**state, "recommendations": recommendations, "briefing": fallback_md, "errors": errors}
    except Exception as e:
        msg = f"briefing: erro na chamada OpenAI — {e}"
        logger.error(msg)
        errors.append(msg)
        fallback_md = (
            f"## {nome} — Briefing NVIDIA Inception\n\n"
            "**Erro:** falha na chamada ao LLM para geração do briefing.\n\n"
            f"### Limitações e Ressalvas\n- {msg}"
        )
        return {**state, "recommendations": recommendations, "briefing": fallback_md, "errors": errors}

    briefing_md: str = str(parsed.get("briefing_md", ""))
    if not briefing_md:
        msg = "briefing: campo briefing_md vazio na resposta do LLM."
        logger.warning(msg)
        errors.append(msg)
        briefing_md = f"## {nome} — Briefing NVIDIA Inception\n\n*(briefing não gerado)*"

    return {
        **state,
        "recommendations": recommendations,
        "briefing": briefing_md,
        "errors": errors,
    }


# ── manual test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import logging as _logging

    _logging.basicConfig(level=_logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    # State fake simulando pipeline completo.
    # nvidia_context com scores baixos (< 0.3) para forçar a seção Limitações.
    fake_state: AgentState = {
        "startup_data": {
            "nome": "Eva",
            "site": "https://evaxai.com",
            "descricao": (
                "Plataforma de cibersegurança que usa LLMs e análise comportamental "
                "para detectar e responder automaticamente a ameaças em tempo real, "
                "sem necessidade de regras manuais."
            ),
            "setor": "cibersegurança",
            "modelo_negocio": "SaaS B2B por assinatura",
            "tecnologias_ia": ["LLM", "análise comportamental", "detecção de anomalias"],
            "tipo_ia": "NLP + detecção de anomalias",
            "founders": ["Ana Lima", "Carlos Souza"],
            "funding": "Seed R$ 2M",
            "clientes_mencionados": ["Banco XYZ", "Seguradora ABC"],
            "status": "enriquecida",
        },
        "retry_count": 1,
        "classification": "AI-native",
        "classification_confidence": 0.85,
        "classification_reasoning": (
            "O produto central é a detecção automática de ameaças via LLM; "
            "sem IA a plataforma não tem funcionalidade."
        ),
        "evidence": [
            "tecnologias_ia inclui 'LLM' e 'detecção de anomalias'",
            "tipo_ia é 'NLP + detecção de anomalias'",
            "descricao mostra resposta automática sem regras manuais",
            "[auditoria] Evidência sustenta AI-native; confidence levemente ajustada "
            "por ausência de nome de modelo específico.",
        ],
        "evidence_validator_verdict": "aceito",
        "gaps_identified": [
            {
                "tag": "latencia_de_inferencia",
                "evidencia": "Dependência de LLM genérico sem otimização de latência para "
                "respostas em tempo real de segurança (janela de detecção crítica)",
            },
            {
                "tag": "governanca_agentes_ia",
                "evidencia": "Ausência de guardrails e governança sobre decisões automatizadas "
                "do modelo, risco regulatório em ambiente financeiro",
            },
            {
                "tag": "contexto_geral",
                "evidencia": "[contexto] Gaps inferidos do uso de LLM via API em contexto de "
                "cibersegurança com clientes no setor financeiro.",
            },
        ],
        "nvidia_context": [
            {
                "texto": (
                    "NeMo Guardrails permite adicionar camadas de segurança e controle "
                    "sobre LLMs, definindo regras de comportamento aceitável para "
                    "aplicações de IA em produção."
                ),
                "fonte": "https://developer.nvidia.com/nemo-guardrails",
                "score": 0.21,
                "tecnologia": "NeMo Guardrails",
            },
            {
                "texto": (
                    "TensorRT-LLM otimiza a inferência de large language models em GPUs "
                    "NVIDIA, reduzindo latência e aumentando throughput em até 8x "
                    "comparado a implementações não otimizadas."
                ),
                "fonte": "https://developer.nvidia.com/tensorrt-llm",
                "score": 0.19,
                "tecnologia": "TensorRT-LLM",
            },
            {
                "texto": (
                    "NVIDIA Morpheus é um framework de cibersegurança acelerado por GPU "
                    "para detecção de ameaças em tempo real em pipelines de dados de rede."
                ),
                "fonte": "https://developer.nvidia.com/morpheus",
                "score": 0.17,
                "tecnologia": "Morpheus",
            },
        ],
        "errors": [
            "rag_node: contexto recuperado com scores baixos — cobertura limitada da "
            "base de conhecimento NVIDIA para o domínio de cibersegurança."
        ],
    }

    result = generate_briefing(fake_state)

    print("\n" + "=" * 70)
    print("BRIEFING MARKDOWN:")
    print("=" * 70)
    print(result.get("briefing", "(vazio)"))

    print("\n" + "=" * 70)
    print("RECOMMENDATIONS:")
    print("=" * 70)
    for i, rec in enumerate(result.get("recommendations") or [], 1):
        print(f"\n[{i}] {rec.get('tecnologia')}")
        print(f"  prioridade   : {rec.get('prioridade')} | complexidade: {rec.get('complexidade')}")
        print(f"  tec          : {rec.get('justificativa_tecnica')}")
        print(f"  negócio      : {rec.get('justificativa_negocio')}")
        print(f"  próxima ação : {rec.get('proxima_acao')}")

    if result.get("errors"):
        print("\n" + "=" * 70)
        print("ERRORS REGISTRADOS:")
        for err in result["errors"]:
            print(f"  ! {err}")

    print()
