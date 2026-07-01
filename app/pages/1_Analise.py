import os
import sys
from datetime import datetime

import streamlit as st
from supabase import create_client

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.run import run_pipeline
from config.settings import settings

st.set_page_config(page_title="Análise de Startup", layout="wide")

# --- Score de Maturidade ---
_DIMENSOES = {
    "Dados": ["alto_volume_dados_tabulares"],
    "Modelos": ["depende_api_externa_atendimento", "latencia_de_inferencia"],
    "Infraestrutura": ["latencia_de_inferencia", "robotica_ou_simulacao"],
    "Governança": ["governanca_agentes_ia", "atua_em_saude"],
    "Produto": ["ausencia_adocao_ia", "voz_call_center_transcricao"],
}


def calcular_score(gaps_identified):
    tags = {g.get("tag") for g in (gaps_identified or []) if g.get("tag") != "contexto_geral"}
    scores = {}
    for dimensao, tags_risco in _DIMENSOES.items():
        encontradas = [t for t in tags_risco if t in tags]
        scores[dimensao] = max(0, 20 - len(encontradas) * 10)
    scores["total"] = sum(scores.values())
    return scores


# --- Guard ---
if "startup_selecionada" not in st.session_state:
    st.warning("Nenhuma startup selecionada. Volte para a página inicial.")
    st.stop()

nome = st.session_state["startup_selecionada"]

# --- Buscar no Supabase ---
client = create_client(settings.supabase_url, settings.supabase_service_role_key)
result = client.table("startups").select("*").eq("nome", nome).execute()
startup_data = result.data[0] if result.data else None

if startup_data is None:
    st.error("Startup não encontrada.")
    st.stop()

ja_analisada = startup_data.get("analysis_status") == "analisada"

# --- Cabeçalho ---
if ja_analisada:
    col_titulo, col_reanalisar, col_voltar = st.columns([5, 1, 1])
else:
    col_titulo, col_voltar = st.columns([6, 1])
    col_reanalisar = None

with col_titulo:
    st.title(nome)

with col_voltar:
    st.write("")
    if st.button("← Voltar"):
        del st.session_state["startup_selecionada"]
        st.switch_page("Home.py")

if ja_analisada and col_reanalisar is not None:
    with col_reanalisar:
        st.write("")
        if st.button("🔄 Re-analisar"):
            with st.spinner("⚙️ Re-analisando... (até 1 minuto)"):
                state = run_pipeline(nome)
            score = calcular_score(state.get("gaps_identified"))
            client.table("startups").update({
                "classification": state.get("classification"),
                "classification_confidence": state.get("classification_confidence"),
                "gaps_identified": state.get("gaps_identified"),
                "recommendations": state.get("recommendations"),
                "briefing": state.get("briefing"),
                "score_maturidade": score,
                "analysis_status": "analisada",
                "analyzed_at": datetime.utcnow().isoformat(),
            }).eq("nome", nome).execute()
            st.session_state["ultimo_state"] = state
            st.session_state["_analise_nome"] = nome
            st.rerun()

# --- Obter state ---
if ja_analisada:
    if "ultimo_state" not in st.session_state or st.session_state.get("_analise_nome") != nome:
        state = {
            "startup_data": startup_data,
            "classification": startup_data.get("classification"),
            "classification_confidence": startup_data.get("classification_confidence"),
            "gaps_identified": startup_data.get("gaps_identified"),
            "recommendations": startup_data.get("recommendations"),
            "briefing": startup_data.get("briefing"),
            "errors": [],
            "evidence_validator_verdict": None,
            "classification_reasoning": None,
        }
        st.session_state["ultimo_state"] = state
        st.session_state["_analise_nome"] = nome
    else:
        state = st.session_state["ultimo_state"]
else:
    st.info("Esta startup ainda não foi analisada pelo batch.")
    if st.button("▶️ Analisar agora"):
        with st.spinner("⚙️ Analisando... (até 1 minuto)"):
            state = run_pipeline(nome)
        st.session_state["ultimo_state"] = state
        st.session_state["_analise_nome"] = nome
    else:
        st.stop()

# --- Erros não-fatais ---
erros = state.get("errors") or []
if erros:
    with st.expander("⚠️ Avisos do pipeline", expanded=False):
        for err in erros:
            st.warning(err)

st.divider()

# ── Seção 1: Classificação ────────────────────────────────────────────────────
st.subheader("Classificação")

classificacao = state.get("classification") or "—"
confidence = state.get("classification_confidence") or 0.0
veredicto = state.get("evidence_validator_verdict") or "—"

_CLS_COLORS = {
    "AI-native": "#2e7d32",
    "AI-enabled": "#f57c00",
    "non-AI": "#757575",
}
cor_cls = _CLS_COLORS.get(classificacao, "#757575")

st.markdown(
    f"<span style='background:{cor_cls};padding:4px 14px;"
    f"border-radius:12px;color:white;font-size:15px;font-weight:bold'>"
    f"{classificacao}</span>",
    unsafe_allow_html=True,
)
st.write("")
st.progress(float(confidence))
st.caption(f"Confiança: {confidence:.0%}")
st.caption(f"Veredicto do validador de evidências: **{veredicto}**")

with st.expander("Ver raciocínio"):
    st.markdown(state.get("classification_reasoning") or "Não disponível.")

st.divider()

# ── Seção 2: Gaps identificados ───────────────────────────────────────────────
st.subheader("Gaps identificados")

gaps_raw = state.get("gaps_identified") or []
gaps = [g for g in gaps_raw if g.get("tag") != "contexto_geral"]

if not gaps:
    st.info("Nenhum gap identificado.")
else:
    for gap in gaps:
        with st.container(border=True):
            st.markdown(f"**{gap.get('tag', '—')}**")
            st.write(gap.get("evidencia") or "Sem descrição.")

st.divider()

# ── Seção 3: Recomendações NVIDIA ─────────────────────────────────────────────
st.subheader("Recomendações NVIDIA")

_PRIO_COLORS = {
    "alta": "#c62828",
    "media": "#ef6c00",
    "média": "#ef6c00",
    "baixa": "#1565c0",
    "baixo": "#1565c0",
}

recomendacoes = state.get("recommendations") or []

if not recomendacoes:
    st.info("Nenhuma recomendação gerada.")
else:
    for rec in recomendacoes:
        tecnologia = rec.get("tecnologia") or "—"
        prioridade = (rec.get("prioridade") or "baixa").lower()
        complexidade = (rec.get("complexidade") or "baixa").lower()
        cor_prio = _PRIO_COLORS.get(prioridade, "#757575")
        cor_comp = _PRIO_COLORS.get(complexidade, "#757575")

        with st.container(border=True):
            st.markdown(f"### {tecnologia}")

            badge_prio = (
                f"<span style='background:{cor_prio};padding:2px 10px;"
                f"border-radius:10px;color:white;font-size:12px'>"
                f"Prioridade: {prioridade}</span>"
            )
            badge_comp = (
                f"<span style='background:{cor_comp};padding:2px 10px;"
                f"border-radius:10px;color:white;font-size:12px'>"
                f"Complexidade: {complexidade}</span>"
            )
            st.markdown(f"{badge_prio}&nbsp;&nbsp;{badge_comp}", unsafe_allow_html=True)
            st.write("")

            st.markdown("**Justificativa técnica:**")
            st.write(rec.get("justificativa_tecnica") or "—")

            st.markdown("**Justificativa de negócio:**")
            st.write(rec.get("justificativa_negocio") or "—")

            st.markdown("**Próxima ação:**")
            st.write(rec.get("proxima_acao") or "—")

st.divider()

# ── Seção 4: Briefing executivo ───────────────────────────────────────────────
st.subheader("Briefing executivo")

briefing = state.get("briefing") or "Briefing não disponível."
st.markdown(briefing)

st.download_button(
    label="⬇️ Baixar briefing (.md)",
    data=briefing,
    file_name=f"{nome}_briefing.md",
    mime="text/markdown",
)

st.divider()

# ── Seção 5: Link para Maturidade ─────────────────────────────────────────────
st.info("💡 Veja o Score de Maturidade desta startup na página ao lado.")
