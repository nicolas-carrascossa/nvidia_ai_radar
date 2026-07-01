import os
import sys

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(page_title="Score de Maturidade", layout="wide")

# --- Guard ---
if "ultimo_state" not in st.session_state:
    st.warning("Nenhuma análise disponível. Execute uma análise primeiro na página Análise.")
    st.stop()

state = st.session_state["ultimo_state"]
nome = (state.get("startup_data") or {}).get("nome", "—")

startup_data = state.get("startup_data") or {}
score_salvo = startup_data.get("score_maturidade")

# --- Mapeamento de dimensões e tags ---
_DIMENSOES = {
    "Dados": ["alto_volume_dados_tabulares"],
    "Modelos": ["depende_api_externa_atendimento", "latencia_de_inferencia"],
    "Infraestrutura": ["latencia_de_inferencia", "robotica_ou_simulacao"],
    "Governança": ["governanca_agentes_ia", "atua_em_saude"],
    "Produto": ["ausencia_adocao_ia", "voz_call_center_transcricao"],
}

# --- gaps_por_dimensao: sempre necessário para a tabela de detalhamento ---
gaps_raw = state.get("gaps_identified") or []
tags_presentes = {g.get("tag") for g in gaps_raw if g.get("tag") != "contexto_geral"}

gaps_por_dimensao = {}
for dimensao, tags_risco in _DIMENSOES.items():
    gaps_por_dimensao[dimensao] = [t for t in tags_risco if t in tags_presentes]

# --- Scores: usar salvo se disponível, senão calcular ---
if score_salvo is not None:
    scores = {k: v for k, v in score_salvo.items() if k != "total"}
    score_total = score_salvo.get("total", sum(scores.values()))
else:
    scores = {}
    for dimensao, tags_risco in _DIMENSOES.items():
        tags_encontradas = gaps_por_dimensao[dimensao]
        scores[dimensao] = max(0, 20 - len(tags_encontradas) * 10)
    score_total = sum(scores.values())

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.title("Score de Maturidade")
st.caption(nome)
st.divider()

# ── Métrica principal ──────────────────────────────────────────────────────────
st.metric("Score de Maturidade", f"{score_total}/100")

if score_total >= 80:
    st.markdown("🟢 **Maturidade Alta** — stack bem desenvolvida")
elif score_total >= 50:
    st.markdown("🟡 **Maturidade Média** — gaps relevantes identificados")
else:
    st.markdown("🔴 **Maturidade Baixa** — múltiplas oportunidades de evolução")

st.divider()

# ── Gráfico Radar ──────────────────────────────────────────────────────────────
dimensoes = list(scores.keys())
valores = list(scores.values())
# fecha o polígono repetindo o primeiro ponto
dimensoes_plot = dimensoes + [dimensoes[0]]
valores_plot = valores + [valores[0]]

fig = go.Figure()
fig.add_trace(
    go.Scatterpolar(
        r=valores_plot,
        theta=dimensoes_plot,
        fill="toself",
        fillcolor="rgba(118,185,0,0.3)",
        line=dict(color="#76b900", width=2),
        name="Maturidade",
    )
)
fig.update_layout(
    polar=dict(
        bgcolor="white",
        radialaxis=dict(
            visible=True,
            range=[0, 20],
            tickvals=[0, 5, 10, 15, 20],
            gridcolor="#e0e0e0",
            linecolor="#e0e0e0",
        ),
        angularaxis=dict(
            gridcolor="#e0e0e0",
            linecolor="#e0e0e0",
        ),
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    showlegend=False,
    margin=dict(t=20, b=20, l=40, r=40),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Tabela de dimensões ────────────────────────────────────────────────────────
st.subheader("Detalhamento por dimensão")

for dimensao, score in scores.items():
    tags_encontradas = gaps_por_dimensao[dimensao]

    if score >= 15:
        cor_score = "#2e7d32"
    elif score >= 10:
        cor_score = "#f57c00"
    else:
        cor_score = "#c62828"

    with st.container(border=True):
        col_nome, col_score, col_gaps = st.columns([2, 1, 3])
        with col_nome:
            st.markdown(f"**{dimensao}**")
        with col_score:
            st.markdown(
                f"<span style='color:{cor_score};font-weight:bold;font-size:16px'>"
                f"{score}/20</span>",
                unsafe_allow_html=True,
            )
        with col_gaps:
            if score == 20:
                st.markdown("✅ Sem gaps identificados")
            else:
                st.markdown(", ".join(f"`{t}`" for t in tags_encontradas))

st.divider()

# ── Dimensão prioritária ───────────────────────────────────────────────────────
st.subheader("Dimensão prioritária para abordagem")

dimensao_min = min(scores, key=lambda d: scores[d])
score_min = scores[dimensao_min]
st.info(
    f"A dimensão **{dimensao_min}** tem o menor score ({score_min}/20), "
    f"indicando maior oportunidade de evolução com tecnologias NVIDIA."
)

st.divider()

st.info("💡 Volte para a página Análise para ver as recomendações completas de tecnologias NVIDIA.")
