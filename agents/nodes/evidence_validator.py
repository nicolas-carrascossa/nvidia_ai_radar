"""
Nó 'evidence_validator' do grafo LangGraph.

Responsabilidade: auditar a classificação produzida pelo nó 'classifier', verificando
se as evidências citadas realmente sustentam a categoria atribuída. Registra seu veredito
em evidence_validator_verdict ("aceito" ou "rebaixado") e ajusta classification_confidence
de acordo.

Este nó NÃO decide o próximo passo do grafo — a lógica condicional de roteamento
(voltar ao classifier ou seguir para gap_analyzer) fica em graph.py.
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
_VALID_VERDICTS = {"aceito", "rebaixado"}

_SYSTEM_PROMPT = """\
Você é um auditor especializado em validar classificações de startups por adoção de IA.

Seu trabalho é revisar a classificação atribuída por um classificador anterior e decidir \
se a evidência apresentada realmente sustenta essa classificação, considerando os dados \
brutos da startup.

CLASSIFICAÇÕES POSSÍVEIS (para referência):
- "AI-native": IA é o produto central — sem ela, o produto não existiria.
- "AI-enabled": IA é uma funcionalidade dentro de um produto que existiria sem ela.
- "non-AI": sinal de IA fraco, vago ou ausente nos dados.

CRITÉRIOS DE AUDITORIA:
- A evidência citada deve ser derivável dos dados brutos fornecidos, não de suposições.
- Uma classification "AI-native" com confidence alta requer tecnologias_ia específicas \
ou tipo_ia concreto nos dados estruturados, não apenas menção genérica a "IA" na descrição.
- Se os campos estruturados (tecnologias_ia, tipo_ia) estão ausentes, a classificação \
depende apenas de texto livre — isso é mais incerto e deve reduzir a confidence mesmo \
que o veredito seja "aceito".
- Se a evidência for vaga, contradiz os dados brutos, ou a confidence original parece \
inflada para a quantidade de dados disponível, emita veredito "rebaixado".

SOBRE CAMPOS ESTRUTURADOS AUSENTES (informado explicitamente no contexto):
- O campo "tecnologias_ia_ausente" indica se o array tecnologias_ia está vazio ou nulo.
- O campo "tipo_ia_ausente" indica se tipo_ia está nulo, vazio ou é "Non-AI".
- Se ambos forem true, a audit_reasoning DEVE mencionar explicitamente que a \
classificação foi baseada apenas em texto livre, sem campos estruturados de IA.
- Se apenas um estiver ausente, também deve ser mencionado.

FORMATO DE SAÍDA — responda SOMENTE com um objeto JSON válido, sem texto antes ou depois, \
sem markdown, sem ```json:
{
  "verdict": "<'aceito' ou 'rebaixado'>",
  "adjusted_confidence": <float entre 0.0 e 1.0>,
  "audit_reasoning": "<explicação curta da decisão de auditoria, 1-3 frases>"
}

Regras para adjusted_confidence:
- Se "aceito": pode manter a confidence original ou ajustá-la levemente (±0.1).
- Se "rebaixado": deve ser sensivelmente menor que a confidence original (redução mínima \
de 0.2, exceto se a original já for muito baixa).\
"""


def _check_structured_fields(startup_data: dict) -> tuple[bool, bool]:
    """Return (tecnologias_ia_ausente, tipo_ia_ausente) as Python booleans."""
    tecnologias = startup_data.get("tecnologias_ia")
    tecnologias_ausente = not tecnologias or len(tecnologias) == 0

    tipo = startup_data.get("tipo_ia")
    tipo_ausente = not tipo or tipo.strip() == "" or tipo.strip() == "Non-AI"

    return tecnologias_ausente, tipo_ausente


def _build_user_message(state: AgentState, tec_ausente: bool, tipo_ausente: bool) -> str:
    sd = state["startup_data"]
    tecnologias = sd.get("tecnologias_ia") or []
    tecnologias_str = ", ".join(tecnologias) if tecnologias else "(não informado)"

    evidence_lines = "\n".join(
        f"  - {e}" for e in (state.get("evidence") or [])
    )

    return (
        "DADOS BRUTOS DA STARTUP:\n"
        f"  nome: {sd.get('nome') or '(não informado)'}\n"
        f"  descricao: {sd.get('descricao') or '(não informado)'}\n"
        f"  setor: {sd.get('setor') or '(não informado)'}\n"
        f"  modelo_negocio: {sd.get('modelo_negocio') or '(não informado)'}\n"
        f"  tecnologias_ia: {tecnologias_str}\n"
        f"  tipo_ia: {sd.get('tipo_ia') or '(não informado)'}\n"
        "\n"
        "CAMPOS ESTRUTURADOS DE IA (calculados antes desta auditoria):\n"
        f"  tecnologias_ia_ausente: {tec_ausente}\n"
        f"  tipo_ia_ausente: {tipo_ausente}\n"
        "\n"
        "CLASSIFICAÇÃO A AUDITAR:\n"
        f"  classification: {state.get('classification')}\n"
        f"  classification_confidence: {state.get('classification_confidence')}\n"
        f"  classification_reasoning: {state.get('classification_reasoning') or '(não informado)'}\n"
        "\n"
        "EVIDÊNCIAS CITADAS PELO CLASSIFICADOR:\n"
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


def validate_evidence(state: AgentState) -> AgentState:
    """LangGraph node: audit the classifier's output and set evidence_validator_verdict."""
    errors: list[str] = list(state.get("errors") or [])
    current_evidence: list[str] = list(state.get("evidence") or [])

    # passo 1 — checagem Python dos campos estruturados
    tec_ausente, tipo_ausente = _check_structured_fields(state["startup_data"])

    oai = OpenAI(api_key=settings.openai_api_key)
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_message(state, tec_ausente, tipo_ausente)},
    ]

    raw = ""
    try:
        raw = _chat_with_retry(oai, messages)
        parsed = json.loads(_strip_fences(raw))
    except json.JSONDecodeError as e:
        msg = f"evidence_validator: JSON inválido na resposta do LLM — {e}. Raw: {raw[:200]}"
        logger.error(msg)
        errors.append(msg)
        return {
            **state,
            "evidence_validator_verdict": "rebaixado",
            "classification_confidence": 0.0,
            "evidence": current_evidence + ["[auditoria falhou: JSON inválido]"],
            "errors": errors,
        }
    except Exception as e:
        msg = f"evidence_validator: erro na chamada OpenAI — {e}"
        logger.error(msg)
        errors.append(msg)
        return {
            **state,
            "evidence_validator_verdict": "rebaixado",
            "classification_confidence": 0.0,
            "evidence": current_evidence + ["[auditoria falhou: erro de API]"],
            "errors": errors,
        }

    # passo 6 — validar verdict
    raw_verdict = parsed.get("verdict", "")
    if raw_verdict not in _VALID_VERDICTS:
        msg = (
            f"evidence_validator: verdict inválido '{raw_verdict}'. "
            "Aplicando fallback para 'rebaixado'."
        )
        logger.warning(msg)
        errors.append(msg)
        raw_verdict = "rebaixado"
        parsed["adjusted_confidence"] = 0.0

    audit_reasoning: str = str(parsed.get("audit_reasoning", ""))
    adjusted_confidence: float = float(parsed.get("adjusted_confidence", 0.0))

    # passo 7 — montar evidence final: original + audit_reasoning como item extra
    updated_evidence = current_evidence + [f"[auditoria] {audit_reasoning}"]

    return {
        **state,
        "evidence_validator_verdict": raw_verdict,
        "classification_confidence": adjusted_confidence,
        "evidence": updated_evidence,
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
        print(f"verdict:             {result.get('evidence_validator_verdict')}")
        print(f"adjusted_confidence: {result.get('classification_confidence'):.2f}")
        print("\nevidence (completa, incluindo audit_reasoning ao final):")
        for item in result.get("evidence") or []:
            print(f"  • {item}")
        if result.get("errors"):
            print("\nerrors:")
            for err in result["errors"]:
                print(f"  ! {err}")

    # ── caso (a): tecnologias_ia preenchido, confidence alta — deve tender a "aceito"
    state_a: AgentState = {
        "startup_data": {
            "nome": "Eva",
            "descricao": (
                "Plataforma de cibersegurança que usa modelos de linguagem (LLMs) e "
                "análise comportamental baseada em machine learning para detectar e "
                "responder automaticamente a ameaças em tempo real, sem necessidade "
                "de regras manuais."
            ),
            "setor": "cibersegurança",
            "modelo_negocio": "SaaS B2B",
            "tecnologias_ia": ["LLM", "machine learning", "análise comportamental"],
            "tipo_ia": "NLP + detecção de anomalias",
            "founders": [],
            "funding": None,
            "clientes_mencionados": [],
            "status": "enriquecida",
        },
        "retry_count": 0,
        "classification": "AI-native",
        "classification_confidence": 0.91,
        "classification_reasoning": (
            "A detecção automática de ameaças via LLM e ML é o produto em si; "
            "sem IA a plataforma não teria funcionalidade central."
        ),
        "evidence": [
            "tecnologias_ia inclui 'LLM', 'machine learning' e 'análise comportamental'",
            "tipo_ia é 'NLP + detecção de anomalias'",
            "descricao menciona resposta automática a ameaças sem regras manuais — dependência direta do modelo",
        ],
    }

    # ── caso (b): tecnologias_ia vazio, confidence moderada — deve mencionar ausência
    #    de campos estruturados; pode ser aceito ou rebaixado dependendo do texto livre
    state_b: AgentState = {
        "startup_data": {
            "nome": "Loginfo",
            "descricao": (
                "Software de gestão logística com módulo de previsão de demanda "
                "e otimização de rotas. Utiliza inteligência artificial para sugerir "
                "consolidações de carga e reduzir custos operacionais."
            ),
            "setor": "logística",
            "modelo_negocio": "SaaS B2B",
            "tecnologias_ia": [],
            "tipo_ia": None,
            "founders": [],
            "funding": None,
            "clientes_mencionados": [],
            "status": "enriquecida",
        },
        "retry_count": 0,
        "classification": "AI-enabled",
        "classification_confidence": 0.68,
        "classification_reasoning": (
            "A IA aparece como módulo de previsão e otimização dentro de um software "
            "de gestão logística que existiria sem ela."
        ),
        "evidence": [
            "descricao menciona 'inteligência artificial' para sugestão de consolidações de carga",
            "descricao menciona módulo de previsão de demanda e otimização de rotas",
            "modelo_negocio é SaaS B2B com produto de gestão logística como core",
        ],
    }

    result_a = validate_evidence(state_a)
    result_b = validate_evidence(state_b)

    _print_result("(a) Eva — tecnologias_ia preenchido, confidence alta", result_a)
    _print_result("(b) Loginfo — tecnologias_ia vazio, confidence moderada", result_b)

    print()
