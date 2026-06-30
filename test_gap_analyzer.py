"""
Teste isolado do nó gap_analyzer com o novo formato de saída estruturado.

Valida que:
1. gaps_identified é list[dict] com chaves "tag" e "evidencia"
2. Todas as tags retornadas estão na lista permitida (exceto "contexto_geral")
3. O último item sempre tem tag "contexto_geral"
4. Nenhuma tag inventada fora da lista é retornada
"""

import json
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

from agents.nodes.gap_analyzer import _ALLOWED_TAGS, analyze_gaps
from agents.state import AgentState

VALID_TAGS = set(_ALLOWED_TAGS) | {"contexto_geral"}


def _check(label: str, result: AgentState) -> bool:
    gaps = result.get("gaps_identified") or []
    errors = result.get("errors") or []

    print(f"\n{'=' * 60}")
    print(f"CASO: {label}")
    print(f"{'=' * 60}")

    ok = True

    # 1. Deve ser lista de dicts
    if not isinstance(gaps, list) or not all(isinstance(g, dict) for g in gaps):
        print("  FALHOU: gaps_identified não é list[dict]")
        ok = False

    # 2. Cada item deve ter as chaves esperadas
    for i, g in enumerate(gaps):
        if "tag" not in g or "evidencia" not in g:
            print(f"  FALHOU: item {i} sem chaves 'tag'/'evidencia': {g}")
            ok = False

    # 3. Último item deve ser contexto_geral
    if gaps and gaps[-1].get("tag") != "contexto_geral":
        print(f"  FALHOU: último item não é contexto_geral — é '{gaps[-1].get('tag')}'")
        ok = False

    # 4. Tags (exceto contexto_geral) devem estar na lista permitida
    for g in gaps:
        tag = g.get("tag")
        if tag not in VALID_TAGS:
            print(f"  FALHOU: tag inválida fora da lista — '{tag}'")
            ok = False

    if ok:
        print("  OK — estrutura válida")

    print("  gaps_identified:")
    for g in gaps:
        print(f"    [{g.get('tag')}] {g.get('evidencia')}")

    if errors:
        print("  errors:")
        for e in errors:
            print(f"    ! {e}")

    return ok


# ── Caso A: AI-native, LLM via API externa em atendimento ────────────────────
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
        "[auditoria] Dependência de API externa é o ponto de atenção.",
    ],
}

# ── Caso B: AI-enabled, dados financeiros tabulares em volume ────────────────
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
        "descricao menciona processamento de milhões de registros tabulares por mês",
        "modelo_negocio de crédito existe independentemente da IA",
    ],
}

# ── Caso C: non-AI ────────────────────────────────────────────────────────────
state_c: AgentState = {
    "startup_data": {
        "nome": "FrioFresh",
        "descricao": (
            "Startup de logística de frios para o setor alimentício. Opera frota "
            "própria de caminhões refrigerados e rastreamento de temperatura via IoT. "
            "Não utiliza modelos de IA atualmente."
        ),
        "setor": "logística",
        "modelo_negocio": "Operador logístico B2B por km rodado",
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
        "descricao afirma explicitamente ausência de IA",
    ],
}

results = {
    "(A) AtendIA — AI-native, LLM via API": analyze_gaps(state_a),
    "(B) CreditoRápido — AI-enabled, dados tabulares": analyze_gaps(state_b),
    "(C) FrioFresh — non-AI, logística": analyze_gaps(state_c),
}

all_ok = all(_check(label, result) for label, result in results.items())

print(f"\n{'=' * 60}")
print("RESULTADO GERAL:", "PASSOU" if all_ok else "FALHOU")
print(f"{'=' * 60}\n")
