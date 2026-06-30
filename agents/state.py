"""
Estado compartilhado do grafo LangGraph para o pipeline de recomendação NVIDIA.

Fluxo dos nós:
    classifier
        ↓
    evidence_validator
        ↓ (condicional)
        ├─ [rebaixado e retry_count < MAX] → volta ao classifier (incrementa retry_count)
        └─ [aceito ou retry esgotado] → gap_analyzer
                                            ↓
                                         rag_node
                                            ↓
                                         briefing
                                            ↓
                                          END

O estado é criado com startup_data e retry_count no início do grafo. Os demais campos
são preenchidos progressivamente por cada nó conforme o grafo avança. Erros não-fatais
(ex: RAG sem resultados relevantes) são registrados em `errors` para que o briefing
final possa mencioná-los sem interromper o fluxo.
"""

from typing import TypedDict


class _AgentStateRequired(TypedDict, total=True):
    """Campos obrigatórios — devem estar presentes desde o início do grafo."""

    startup_data: dict
    """Dados brutos da startup vindos do Supabase.
    Campos esperados: nome, site, descricao, setor, modelo_negocio,
    tecnologias_ia, tipo_ia, founders, funding, clientes_mencionados, status."""

    retry_count: int
    """Quantas vezes o fluxo já voltou do evidence_validator para o classifier.
    Começa em 0 na criação do estado."""


class AgentState(_AgentStateRequired, total=False):
    """Estado completo do grafo — combina campos obrigatórios e progressivos."""

    classification: str
    """Classificação da startup: "AI-native", "AI-enabled" ou "non-AI"."""

    classification_confidence: float
    """Confiança da classificação, de 0.0 a 1.0."""

    classification_reasoning: str
    """Justificativa textual do classifier, usada para auditoria humana."""

    evidence: list[str]
    """Evidências textuais extraídas dos dados da startup que sustentam (ou refutam)
    a classificação atribuída."""

    evidence_validator_verdict: str
    """Decisão do evidence_validator: "aceito" ou "rebaixado"."""

    gaps_identified: list[dict]
    """Gaps técnicos prováveis inferidos pelo gap_analyzer com base no perfil da startup.
    Cada item: {"tag": str, "evidencia": str}. O item de contexto usa tag "contexto_geral"."""

    nvidia_context: list[dict]
    """Chunks recuperados do RAG. Cada item deve conter ao menos:
    {"texto": str, "fonte": str, "score": float}."""

    recommendations: list[dict]
    """Tecnologias NVIDIA recomendadas. Cada item deve conter:
    {"tecnologia": str, "justificativa_tecnica": str, "justificativa_negocio": str,
     "proxima_acao": str, "prioridade": str, "complexidade": str}."""

    briefing: str
    """Relatório final em texto/markdown gerado pelo nó briefing."""

    errors: list[str]
    """Erros não-fatais registrados por qualquer nó durante a execução.
    O grafo continua mesmo com entradas nesta lista; o briefing final
    deve consultá-la para indicar limitações no relatório."""
