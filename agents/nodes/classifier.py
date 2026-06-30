"""
Nó 'classifier' do grafo LangGraph.

Responsabilidade: receber um AgentState com startup_data preenchido e classificar
a startup em uma de três categorias mutuamente exclusivas, preenchendo os campos
classification, classification_confidence, classification_reasoning e evidence.

Este nó é chamado novamente pelo grafo se o evidence_validator rebaixar a
classificação e retry_count ainda não tiver atingido o limite máximo.
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
_VALID_CLASSIFICATIONS = {"AI-native", "AI-enabled", "non-AI"}

_SYSTEM_PROMPT = """\
Você é um analista especializado em classificar startups brasileiras por seu grau de \
adoção de Inteligência Artificial. Sua tarefa é classificar uma startup em EXATAMENTE \
uma das três categorias abaixo — sem criar subcategorias, sem combinar categorias, \
sem inventar termos novos.

CATEGORIAS (definições obrigatórias):

1. "AI-native"
   A IA é o produto central da startup. Sem o componente de IA, o produto ou serviço \
simplesmente não existiria. Indicadores típicos: tecnologias_ia específicas e nomeadas \
(não termos genéricos como "IA" ou "machine learning" sem mais detalhes), tipo_ia \
preenchido com algo concreto (ex: "NLP", "visão computacional", "LLM"), e a descrição \
deixa claro que o núcleo do negócio é o modelo ou algoritmo em si.

2. "AI-enabled"
   A startup usa IA como uma funcionalidade dentro de um produto que existiria sem ela. \
O negócio principal é outro (SaaS, marketplace, serviço profissional, etc.) e a IA é \
um componente adicionado para melhorar ou automatizar parte do produto — como um chatbot \
de suporte, recomendação de conteúdo, ou feature de análise preditiva.

3. "non-AI"
   O sinal de IA nos dados é fraco, vago ou ausente. Pode ser um falso positivo do filtro \
de palavras-chave usado na coleta. Inclui casos em que IA aparece apenas no contexto \
de tendências do setor, sem indicar adoção real pelo produto da startup.

REGRAS DE CLASSIFICAÇÃO:
- Baseie-se SOMENTE nos dados fornecidos. Não invente informações sobre a startup.
- Se os dados estiverem incompletos (campos vazios ou None), classifique com a informação \
disponível e reduza a confidence proporcionalmente — quanto menos dados, menor a confidence.
- Evidências devem citar dados presentes nos campos fornecidos, nunca suposições.

FORMATO DE SAÍDA — responda SOMENTE com um objeto JSON válido, sem texto antes ou depois, \
sem markdown, sem ```json:
{
  "classification": "<uma das três categorias exatas>",
  "confidence": <float entre 0.0 e 1.0>,
  "reasoning": "<1 a 3 frases explicando a classificação>",
  "evidence": ["<dado específico dos campos que sustenta a classificação>", ...]
}

O campo evidence deve conter de 2 a 5 strings, cada uma citando um dado concreto dos \
campos fornecidos (ex: 'tecnologias_ia inclui \"GPT-4\" e \"embeddings\"', \
'tipo_ia é \"NLP\"', 'descricao menciona modelo treinado em dados proprietários').\
"""


def _build_user_message(startup_data: dict) -> str:
    """Format the startup fields relevant to classification into the user message."""
    fields = {
        "nome": startup_data.get("nome") or "(não informado)",
        "descricao": startup_data.get("descricao") or "(não informado)",
        "setor": startup_data.get("setor") or "(não informado)",
        "modelo_negocio": startup_data.get("modelo_negocio") or "(não informado)",
        "tecnologias_ia": startup_data.get("tecnologias_ia") or [],
        "tipo_ia": startup_data.get("tipo_ia") or "(não informado)",
    }
    tecnologias_str = (
        ", ".join(fields["tecnologias_ia"]) if fields["tecnologias_ia"] else "(não informado)"
    )
    return (
        f"nome: {fields['nome']}\n"
        f"descricao: {fields['descricao']}\n"
        f"setor: {fields['setor']}\n"
        f"modelo_negocio: {fields['modelo_negocio']}\n"
        f"tecnologias_ia: {tecnologias_str}\n"
        f"tipo_ia: {fields['tipo_ia']}"
    )


def _strip_fences(text: str) -> str:
    """Remove ```json ... ``` or ``` ... ``` wrappers the LLM sometimes adds."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _chat_with_retry(oai: OpenAI, messages: list[dict]) -> str:
    """Call the OpenAI chat API with up to 3 retries on transient errors."""
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


def classify_startup(state: AgentState) -> AgentState:
    """LangGraph node: classify the startup and populate classification fields."""
    startup_data = state["startup_data"]
    errors: list[str] = list(state.get("errors") or [])

    oai = OpenAI(api_key=settings.openai_api_key)

    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_message(startup_data)},
    ]

    raw = ""
    try:
        raw = _chat_with_retry(oai, messages)
        parsed = json.loads(_strip_fences(raw))
    except json.JSONDecodeError as e:
        msg = f"classifier: JSON inválido na resposta do LLM — {e}. Raw: {raw[:200]}"
        logger.error(msg)
        errors.append(msg)
        return {
            **state,
            "classification": "non-AI",
            "classification_confidence": 0.0,
            "classification_reasoning": "Falha ao parsear resposta do classificador.",
            "evidence": [],
            "errors": errors,
        }
    except Exception as e:
        msg = f"classifier: erro na chamada OpenAI — {e}"
        logger.error(msg)
        errors.append(msg)
        return {
            **state,
            "classification": "non-AI",
            "classification_confidence": 0.0,
            "classification_reasoning": "Falha na chamada ao classificador.",
            "evidence": [],
            "errors": errors,
        }

    raw_classification = parsed.get("classification", "")
    if raw_classification not in _VALID_CLASSIFICATIONS:
        msg = (
            f"classifier: valor inválido em 'classification': '{raw_classification}'. "
            "Aplicando fallback para 'non-AI'."
        )
        logger.warning(msg)
        errors.append(msg)
        raw_classification = "non-AI"
        parsed["confidence"] = 0.0

    return {
        **state,
        "classification": raw_classification,
        "classification_confidence": float(parsed.get("confidence", 0.0)),
        "classification_reasoning": str(parsed.get("reasoning", "")),
        "evidence": list(parsed.get("evidence") or []),
        "errors": errors,
    }


# ── manual test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    STARTUP_NAME = "Eva"  # troque aqui para testar outra startup

    from supabase import create_client

    client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    result = client.table("startups").select("*").eq("nome", STARTUP_NAME).limit(1).execute()

    if not result.data:
        print(f"Startup '{STARTUP_NAME}' não encontrada no banco.")
        sys.exit(1)

    startup_row = result.data[0]
    print(f"Startup encontrada: {startup_row['nome']} (status: {startup_row.get('status')})\n")

    initial_state: AgentState = {
        "startup_data": startup_row,
        "retry_count": 0,
    }

    final_state = classify_startup(initial_state)

    print(f"classification:  {final_state['classification']}")
    print(f"confidence:      {final_state['classification_confidence']:.2f}")
    print(f"reasoning:       {final_state['classification_reasoning']}")
    print("\nevidence:")
    for ev in final_state.get("evidence") or []:
        print(f"  • {ev}")
    if final_state.get("errors"):
        print("\nerrors:")
        for err in final_state["errors"]:
            print(f"  ! {err}")
