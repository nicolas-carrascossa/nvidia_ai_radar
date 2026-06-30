"""
Nó 'gap_analyzer' do grafo LangGraph.

Responsabilidade: inferir gaps técnicos ou oportunidades de adoção de IA PROVÁVEIS
na stack da startup, a partir do perfil coletado no Supabase. As inferências são
hipóteses plausíveis — não fatos confirmados — porque o banco não contém dados diretos
de latência, custo, governança ou arquitetura interna.

Este nó roda para qualquer classification (AI-native, AI-enabled, non-AI) e não cita
produtos NVIDIA — a solução é responsabilidade dos nós rag_node e briefing.
"""

import json
import logging
import re
import time

from openai import OpenAI

from agents.state import AgentState
from config.settings import settings

logger = logging.getLogger(__name__)

_MODEL = "gpt-4o-mini"
_RETRY_DELAYS = [5, 10, 20]

_ALLOWED_TAGS = [
    "depende_api_externa_atendimento",
    "alto_volume_dados_tabulares",
    "voz_call_center_transcricao",
    "atua_em_saude",
    "robotica_ou_simulacao",
    "latencia_de_inferencia",
    "governanca_agentes_ia",
    "ausencia_adocao_ia",
]

_SYSTEM_PROMPT = """\
Você é um arquiteto de IA especializado em diagnosticar gaps técnicos e oportunidades \
de adoção de IA em startups brasileiras.

Seu trabalho é analisar o perfil de uma startup e inferir gaps PROVÁVEIS na sua stack \
de IA ou oportunidades de adoção. Estas são HIPÓTESES PLAUSÍVEIS derivadas dos dados \
disponíveis — não fatos confirmados.

TAGS PERMITIDAS — escolha SOMENTE entre as tags abaixo. NÃO invente tags fora dessa lista:
- depende_api_externa_atendimento: startup usa LLMs via APIs externas (OpenAI, Anthropic, \
etc.) sem otimização própria — gap: custo, latência, dependência de fornecedor, ausência \
de observabilidade e governança.
- alto_volume_dados_tabulares: startup processa grandes volumes de dados tabulares \
(fintech, analytics) — gap: aceleração de pipeline, processamento ineficiente em CPU.
- voz_call_center_transcricao: startup faz voz, call center, transcrição ou atendimento \
por voz — gap: infraestrutura dedicada de voz (ASR/TTS), latência de reconhecimento.
- atua_em_saude: startup atua em saúde/healthcare — gap: compliance, governança de modelos, \
modelos especializados de domínio clínico.
- robotica_ou_simulacao: startup faz robótica, simulação ou gêmeos digitais — gap: \
infraestrutura de simulação e aceleração, ambientes de treinamento em escala.
- latencia_de_inferencia: startup menciona (explícita ou implicitamente) problemas de \
latência de inferência — gap: otimização de serving, quantização, batching.
- governanca_agentes_ia: startup com agentes de IA autônomos ou tomada de decisão \
automatizada — gap: guardrails, rastreabilidade de decisões.
- ausencia_adocao_ia: startup "non-AI" ou sem adoção clara de IA — registrar como \
ausência de adoção com oportunidade específica ao setor. NÃO force gap técnico de stack \
que não se aplica. Use também como fallback se nenhuma outra tag se aplicar com clareza.

REGRAS IMPORTANTES:
- NÃO mencione produtos, plataformas ou soluções específicas de fornecedores (NVIDIA, \
AWS, Google, OpenAI, etc.) — descreva apenas o problema/gap, não a solução.
- Baseie as inferências nos dados fornecidos. Se os dados forem escassos, diga isso \
no gap_reasoning.
- Gere de 1 a 4 gaps. Prefira menos gaps com mais precisão a muitos gaps genéricos.
- Se nenhuma tag se aplicar com clareza, use "ausencia_adocao_ia" como fallback.

FORMATO DE SAÍDA — responda SOMENTE com um objeto JSON válido, sem texto antes ou depois, \
sem markdown, sem ```json:
{
  "gaps": [
    {
      "tag": "<uma das tags permitidas acima, em snake_case>",
      "evidencia": "<string curta explicando por que esse gap se aplica a esta startup>"
    }
  ],
  "gap_reasoning": "<justificativa curta (1-3 frases) conectando os gaps inferidos \
aos dados da startup, mencionando o caráter hipotético das inferências>"
}\
"""


def _build_user_message(state: AgentState) -> str:
    sd = state["startup_data"]
    tecnologias = sd.get("tecnologias_ia") or []
    tecnologias_str = ", ".join(tecnologias) if tecnologias else "(não informado)"

    evidence_lines = "\n".join(
        f"  - {e}" for e in (state.get("evidence") or [])
    )

    return (
        "PERFIL DA STARTUP:\n"
        f"  nome: {sd.get('nome') or '(não informado)'}\n"
        f"  descricao: {sd.get('descricao') or '(não informado)'}\n"
        f"  setor: {sd.get('setor') or '(não informado)'}\n"
        f"  modelo_negocio: {sd.get('modelo_negocio') or '(não informado)'}\n"
        f"  tecnologias_ia: {tecnologias_str}\n"
        f"  tipo_ia: {sd.get('tipo_ia') or '(não informado)'}\n"
        "\n"
        "CLASSIFICAÇÃO (produzida e auditada pelos nós anteriores):\n"
        f"  classification: {state.get('classification')}\n"
        f"  classification_confidence: {state.get('classification_confidence')}\n"
        "\n"
        "EVIDÊNCIAS E AUDITORIA ANTERIORES:\n"
        f"{evidence_lines or '  (nenhuma)'}"
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


def analyze_gaps(state: AgentState) -> AgentState:
    """LangGraph node: infer probable technical gaps and populate gaps_identified."""
    errors: list[str] = list(state.get("errors") or [])

    oai = OpenAI(api_key=settings.openai_api_key)
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_message(state)},
    ]

    _FALLBACK: list[dict] = [
        {"tag": "ausencia_adocao_ia", "evidencia": "Dados insuficientes para inferir gaps técnicos específicos"}
    ]

    raw = ""
    try:
        raw = _chat_with_retry(oai, messages)
        parsed = json.loads(_strip_fences(raw))
    except json.JSONDecodeError as e:
        msg = f"gap_analyzer: JSON inválido na resposta do LLM — {e}. Raw: {raw[:200]}"
        logger.error(msg)
        errors.append(msg)
        return {
            **state,
            "gaps_identified": _FALLBACK,
            "errors": errors,
        }
    except Exception as e:
        msg = f"gap_analyzer: erro na chamada OpenAI — {e}"
        logger.error(msg)
        errors.append(msg)
        return {
            **state,
            "gaps_identified": _FALLBACK,
            "errors": errors,
        }

    gaps: list[dict] = parsed.get("gaps") or []
    gap_reasoning: str = str(parsed.get("gap_reasoning", ""))

    # Valida que cada item tem as chaves esperadas e tag permitida; descarta inválidos
    valid_gaps: list[dict] = []
    for item in gaps:
        if not isinstance(item, dict):
            continue
        tag = item.get("tag", "")
        if tag not in _ALLOWED_TAGS:
            logger.warning("gap_analyzer: tag '%s' não está na lista permitida — descartada.", tag)
            continue
        valid_gaps.append({"tag": tag, "evidencia": str(item.get("evidencia", ""))})

    if not valid_gaps:
        msg = "gap_analyzer: LLM retornou lista de gaps vazia ou sem tags válidas."
        logger.warning(msg)
        errors.append(msg)
        valid_gaps = _FALLBACK

    gaps_identified: list[dict] = valid_gaps + [
        {"tag": "contexto_geral", "evidencia": f"[contexto] {gap_reasoning}"}
    ]

    return {
        **state,
        "gaps_identified": gaps_identified,
        "errors": errors,
    }


# ── manual test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import logging as _logging

    _logging.basicConfig(level=_logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    def _print_result(label: str, result: AgentState) -> None:
        print(f"\n{'='*60}")
        print(f"CASO: {label}")
        print(f"{'='*60}")
        print("gaps_identified:")
        for item in result.get("gaps_identified") or []:
            print(f"  • {item}")
        if result.get("errors"):
            print("\nerrors:")
            for err in result["errors"]:
                print(f"  ! {err}")

    # ── caso (a): AI-native usando LLM via API externa em atendimento
    state_a: AgentState = {
        "startup_data": {
            "nome": "AtendIA",
            "descricao": (
                "Plataforma de atendimento ao cliente automatizado que usa GPT-4 via API "
                "da OpenAI para responder tickets, classificar intenção e escalar para "
                "humanos quando necessário. Processa mais de 50 mil conversas por dia."
            ),
            "setor": "tecnologia",
            "modelo_negocio": "SaaS B2B por volume de tickets",
            "tecnologias_ia": ["GPT-4", "embeddings", "classificação de intenção"],
            "tipo_ia": "NLP / LLM",
            "founders": [],
            "funding": None,
            "clientes_mencionados": [],
            "status": "enriquecida",
        },
        "retry_count": 0,
        "classification": "AI-native",
        "classification_confidence": 0.88,
        "evidence": [
            "tecnologias_ia inclui 'GPT-4' e 'embeddings'",
            "tipo_ia é 'NLP / LLM'",
            "descricao mostra que o produto central é atendimento automatizado via LLM",
            "[auditoria] Classificação sustentada pelos dados estruturados; "
            "dependência de API externa é o ponto de atenção.",
        ],
    }

    # ── caso (b): AI-enabled processando dados financeiros tabulares em volume
    state_b: AgentState = {
        "startup_data": {
            "nome": "CreditoRápido",
            "descricao": (
                "Fintech de concessão de crédito para PMEs. Analisa histórico financeiro, "
                "fluxo de caixa e dados de bureaus de crédito para gerar score de risco "
                "e aprovar empréstimos em minutos. Processa milhões de registros tabulares "
                "por mês para recalibrar os modelos preditivos."
            ),
            "setor": "finanças",
            "modelo_negocio": "Fintech de crédito, receita por spread e taxa de originação",
            "tecnologias_ia": ["modelos preditivos", "score de risco"],
            "tipo_ia": "machine learning supervisionado",
            "founders": [],
            "funding": "Série A",
            "clientes_mencionados": [],
            "status": "enriquecida",
        },
        "retry_count": 0,
        "classification": "AI-enabled",
        "classification_confidence": 0.74,
        "evidence": [
            "tecnologias_ia inclui 'modelos preditivos' e 'score de risco'",
            "descricao menciona processamento de milhões de registros tabulares por mês",
            "modelo_negocio de crédito existe independentemente da IA",
            "[auditoria] Evidência sustenta AI-enabled; volume de dados tabulares é dado "
            "relevante para gaps de infraestrutura.",
        ],
    }

    # ── caso (c): non-AI — deve gerar gap do tipo "ausência de adoção", não gap técnico
    state_c: AgentState = {
        "startup_data": {
            "nome": "FrioFresh",
            "descricao": (
                "Startup de logística de frios para o setor alimentício. Opera frota "
                "própria de caminhões refrigerados e oferece rastreamento de temperatura "
                "em tempo real via IoT. Não utiliza modelos de IA atualmente."
            ),
            "setor": "logística",
            "modelo_negocio": "Operador logístico B2B por km rodado e tonelada transportada",
            "tecnologias_ia": [],
            "tipo_ia": None,
            "founders": [],
            "funding": None,
            "clientes_mencionados": [],
            "status": "enriquecida",
        },
        "retry_count": 0,
        "classification": "non-AI",
        "classification_confidence": 0.82,
        "evidence": [
            "tecnologias_ia está vazio",
            "tipo_ia não informado",
            "descricao afirma explicitamente ausência de IA",
            "[auditoria] Classificação 'non-AI' é correta e bem sustentada pelos dados; "
            "empresa tem IoT mas sem camada de IA sobre os dados.",
        ],
    }

    result_a = analyze_gaps(state_a)
    result_b = analyze_gaps(state_b)
    result_c = analyze_gaps(state_c)

    _print_result("(a) AtendIA — AI-native, LLM via API externa", result_a)
    _print_result("(b) CreditoRápido — AI-enabled, dados financeiros tabulares", result_b)
    _print_result("(c) FrioFresh — non-AI, logística de frios sem IA", result_c)

    print()
