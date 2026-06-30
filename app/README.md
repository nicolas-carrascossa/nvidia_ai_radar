# Interface Web — Fase 5

## Visão geral

Esta fase implementa o frontend do NVIDIA Startup AI Radar usando Streamlit, conectando todas as fases anteriores (scraping, RAG, multiagente, motor de recomendação) numa interface web interativa. O resultado é uma plataforma navegável que permite descobrir startups brasileiras de IA, executar o pipeline de análise completo e visualizar recomendações de tecnologias NVIDIA com um score de maturidade técnica.

## Estrutura de arquivos

```
app/
  Home.py                    # Página 1 — Radar de Startups
  pages/
    1_Analise.py             # Página 2 — Análise individual
    2_Maturidade.py          # Página 3 — Score de Maturidade (diferencial)
  components/
    startup_card.py
    recommendation_card.py
    radar_chart.py
```

## Como rodar

```bash
cd raiz do projeto
streamlit run app/Home.py
```

## Páginas

### Página 1 — Radar de Startups (Home.py)
- Lista todas as startups do Supabase
- Filtros por nome, setor e status na sidebar
- Cards com badge de status colorido e tecnologias de IA
- Botão "Analisar" navega para a análise individual

### Página 2 — Análise Individual (1_Analise.py)
- Executa o pipeline multiagente completo via `run_pipeline()`
- Exibe classificação AI-native com score de confiança
- Lista gaps técnicos identificados
- Cards de recomendações NVIDIA com prioridade e complexidade
- Briefing executivo completo em markdown com download em `.md`
- Cache do resultado: re-visitar a mesma startup não re-executa o pipeline

### Página 3 — Score de Maturidade (2_Maturidade.py)
- Diferencial do projeto
- Calcula score de 0 a 100 em 5 dimensões: Dados, Modelos, Infraestrutura, Governança, Produto
- Score por dimensão baseado nos gaps identificados pelo pipeline
- Gráfico radar interativo com Plotly
- Identifica a dimensão prioritária para abordagem NVIDIA

## Dependências

```
streamlit>=1.28.0
plotly>=5.0.0
```

## Observações técnicas

- O frontend não reimplementa nenhuma lógica de IA — apenas consome o que foi construído nas fases anteriores
- `st.session_state["ultimo_state"]` transfere o AgentState entre as páginas 2 e 3 sem re-executar o pipeline
- O pipeline pode levar até 60 segundos por startup dependendo da disponibilidade das APIs
