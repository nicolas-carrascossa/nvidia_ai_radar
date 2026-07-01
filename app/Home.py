import os
import sys

import streamlit as st
from supabase import create_client

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import settings

st.set_page_config(page_title="NVIDIA Startup AI Radar", layout="wide")

st.markdown("""
<div style='
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    border-left: 5px solid #76b900;
    border-radius: 8px;
    padding: 28px 32px;
    margin-bottom: 24px;
'>
    <div style='color:#76b900;font-size:11px;font-weight:700;
                letter-spacing:3px;text-transform:uppercase;
                margin-bottom:8px'>
        NVIDIA Inception Program
    </div>
    <div style='color:white;font-size:32px;font-weight:800;
                line-height:1.2;margin-bottom:8px'>
        Startup AI Radar
    </div>
    <div style='color:#aaaaaa;font-size:14px'>
        Mapeamento de startups brasileiras AI-native para o time de Startups & VCs
    </div>
</div>
""", unsafe_allow_html=True)

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

# --- Métricas ---
analisadas = len([s for s in filtradas if s.get("analysis_status") == "analisada"])
ai_native = len([s for s in filtradas if s.get("classification") == "AI-native"])
ai_enabled = len([s for s in filtradas if s.get("classification") == "AI-enabled"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total", len(filtradas))
col2.metric("Analisadas", analisadas)
col3.metric("AI-native", ai_native)
col4.metric("AI-enabled", ai_enabled)

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
