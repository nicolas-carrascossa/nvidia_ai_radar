"""
Teste isolado do recommendation_engine (Fase 4).

Mocka gaps_identified (formato produzido pelo gap_analyzer pós-refatoração) e
nvidia_context (formato produzido pelo rag_node), chama generate_recommendations()
e imprime o resultado de forma legível para validação manual.
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

from agents.recommendation_engine import _determine_base_recommendations, generate_recommendations

# gaps com tags reais — 'depende_api_externa_atendimento' aparece 1x, mas junto com
# 'latencia_de_inferencia' eles compartilham 'Triton' -> deve virar prioridade Alta pra Triton
gaps_identified: list[dict] = [
    {
        "tag": "depende_api_externa_atendimento",
        "evidencia": "Startup usa GPT-4 via API da OpenAI para atendimento, sem camada própria de serving.",
    },
    {
        "tag": "alto_volume_dados_tabulares",
        "evidencia": "Processa milhões de registros tabulares por mês para recalibrar modelos preditivos.",
    },
    {
        "tag": "latencia_de_inferencia",
        "evidencia": "Atendimento em tempo real depende de resposta rápida do modelo, sensível a latência.",
    },
    {
        "tag": "contexto_geral",
        "evidencia": "[contexto] Inferências baseadas em descrição textual da startup; dados de infraestrutura real não confirmados.",
    },
]

nvidia_context: list[dict] = [
    {
        "texto": "NVIDIA NIM oferece microsserviços de inferência otimizados para deploy de LLMs "
        "em produção, reduzindo dependência de APIs externas de terceiros e dando controle "
        "sobre custo e latência.",
        "fonte": "https://www.nvidia.com/nim",
        "score": 0.91,
        "tecnologia": "NIM",
    },
    {
        "texto": "NVIDIA Triton Inference Server permite servir múltiplos modelos com batching "
        "dinâmico, reduzindo latência de inferência em cargas de produção.",
        "fonte": "https://www.nvidia.com/triton",
        "score": 0.87,
        "tecnologia": "Triton",
    },
    {
        "texto": "RAPIDS e cuDF aceleram pipelines de dados tabulares em GPU, com ganhos de "
        "performance de até 10x sobre processamento tradicional em CPU para grandes volumes.",
        "fonte": "https://www.nvidia.com/rapids",
        "score": 0.83,
        "tecnologia": "RAPIDS",
    },
]


def main() -> None:
    print("=" * 70)
    print("ETAPA 1 — cálculo determinístico (_determine_base_recommendations)")
    print("=" * 70)
    base = _determine_base_recommendations(gaps_identified)
    for tech, info in base.items():
        print(f"  {tech:20s} prioridade={info['prioridade']:6s} complexidade={info['complexidade']:6s} gap_count={info['gap_count']}")

    print()
    print("=" * 70)
    print("ETAPA 2 — generate_recommendations() (com chamada ao LLM)")
    print("=" * 70)
    recommendations = generate_recommendations(gaps_identified, nvidia_context)

    if not recommendations:
        print("  (vazio — nenhuma recomendação gerada, verifique logs acima)")
        return

    for rec in recommendations:
        print(f"\n--- {rec['tecnologia']} ---")
        print(f"  prioridade        : {rec['prioridade']}")
        print(f"  complexidade      : {rec['complexidade']}")
        print(f"  justificativa_tecnica : {rec['justificativa_tecnica']}")
        print(f"  justificativa_negocio : {rec['justificativa_negocio']}")
        print(f"  proxima_acao           : {rec['proxima_acao']}")

    print()


if __name__ == "__main__":
    main()
