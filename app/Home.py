import os
import sys

import streamlit as st
from supabase import create_client

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import settings

st.set_page_config(page_title="NVIDIA Startup AI Radar", layout="wide")

st.title("NVIDIA Startup AI Radar")
st.caption("Descubra e analise startups brasileiras de IA com tecnologias NVIDIA.")

# --- Conexão e busca ---
try:
    client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    result = client.table("startups").select("*").execute()
    startups = result.data or []
except Exception as e:
    st.error(f"Erro ao buscar startups: {e}")
    st.stop()

# --- Sidebar: filtros ---
with st.sidebar:
    st.header("Filtros")

    busca_nome = st.text_input("Buscar por nome", placeholder="Ex: Neuralmind")

    setores_disponiveis = sorted({s["setor"] for s in startups if s.get("setor")})
    filtro_setor = st.multiselect("Setor", options=setores_disponiveis)

    status_disponiveis = sorted({s["status"] for s in startups if s.get("status")})
    filtro_status = st.multiselect("Status", options=status_disponiveis)

    filtro_classification = st.multiselect(
        "Classificação IA",
        options=["AI-native", "AI-enabled", "non-AI"],
    )

    filtro_analysis = st.multiselect(
        "Status de análise",
        options=["analisada", "pendente", "falhou"],
    )

# --- Aplicar filtros ---
filtradas = startups

if busca_nome:
    termo = busca_nome.lower()
    filtradas = [s for s in filtradas if termo in (s.get("nome") or "").lower()]

if filtro_setor:
    filtradas = [s for s in filtradas if s.get("setor") in filtro_setor]

if filtro_status:
    filtradas = [s for s in filtradas if s.get("status") in filtro_status]

if filtro_classification:
    filtradas = [s for s in filtradas if s.get("classification") in filtro_classification]

if filtro_analysis:
    filtradas = [s for s in filtradas if s.get("analysis_status") in filtro_analysis]

# --- Métrica ---
st.metric("Startups encontradas", len(filtradas))
st.divider()

# --- Grade de cards ---
if not filtradas:
    st.info("Nenhuma startup encontrada com os filtros selecionados.")
else:
    _STATUS_COLORS = {
        "enriquecida": "#2e7d32",
        "parcial": "#f57c00",
    }
    _CLS_COLORS = {
        "AI-native": "#2e7d32",
        "AI-enabled": "#f57c00",
        "non-AI": "#757575",
    }

    cols = st.columns(3)
    for i, startup in enumerate(filtradas):
        col = cols[i % 3]
        with col:
            with st.container(border=True):
                nome = startup.get("nome") or "Sem nome"
                setor = startup.get("setor") or "Não informado"
                status = startup.get("status") or "desconhecido"
                tecnologias = startup.get("tecnologias_ia") or []
                classification = startup.get("classification")
                score_maturidade = startup.get("score_maturidade")

                st.markdown(f"**{nome}**")
                st.write(setor)

                cor = _STATUS_COLORS.get(status, "#757575")
                st.markdown(
                    f"<span style='background:{cor};padding:2px 8px;"
                    f"border-radius:10px;color:white;font-size:12px'>{status}</span>",
                    unsafe_allow_html=True,
                )

                if classification:
                    cor_cls = _CLS_COLORS.get(classification, "#757575")
                    st.markdown(
                        f"<span style='background:{cor_cls};padding:2px 8px;"
                        f"border-radius:10px;color:white;font-size:12px'>{classification}</span>",
                        unsafe_allow_html=True,
                    )

                if score_maturidade is not None:
                    st.caption(f"Score: {score_maturidade.get('total', '—')}/100")

                if tecnologias:
                    st.caption(", ".join(tecnologias[:3]))

                if st.button("🔍 Analisar", key=f"analisar_{i}"):
                    st.session_state["startup_selecionada"] = nome
                    st.switch_page("pages/1_Analise.py")
