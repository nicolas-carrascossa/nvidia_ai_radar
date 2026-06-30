import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from supabase import create_client

from config.settings import settings
from agents.run import run_pipeline

# ── Score de Maturidade ────────────────────────────────────────────────────────

_DIMENSOES = {
    "Dados": ["alto_volume_dados_tabulares"],
    "Modelos": ["depende_api_externa_atendimento", "latencia_de_inferencia"],
    "Infraestrutura": ["latencia_de_inferencia", "robotica_ou_simulacao"],
    "Governança": ["governanca_agentes_ia", "atua_em_saude"],
    "Produto": ["ausencia_adocao_ia", "voz_call_center_transcricao"],
}


def calcular_score(gaps_identified: list) -> dict:
    tags = {g.get("tag") for g in (gaps_identified or []) if g.get("tag") != "contexto_geral"}
    scores = {}
    for dimensao, tags_risco in _DIMENSOES.items():
        encontradas = [t for t in tags_risco if t in tags]
        scores[dimensao] = max(0, 20 - len(encontradas) * 10)
    scores["total"] = sum(scores.values())
    return scores


# ── Pipeline batch ─────────────────────────────────────────────────────────────

def main():
    client = create_client(settings.supabase_url, settings.supabase_service_role_key)

    result = client.table("startups").select("nome, analysis_status").execute()
    todas = result.data or []

    pendentes = [
        r["nome"] for r in todas
        if r.get("analysis_status") in ("pendente", None)
    ]

    if not pendentes:
        print("Nenhuma startup pendente.", flush=True)
        return

    total = len(pendentes)
    print(f"Iniciando batch: {total} startups para analisar", flush=True)
    print(f"Tempo estimado: ~{total * 60 // 60} minutos", flush=True)
    print(flush=True)

    sucessos = 0
    falhas = 0

    for i, nome in enumerate(pendentes):
        print(f"[{i+1}/{total}] Analisando: {nome}...", flush=True)
        try:
            state = run_pipeline(nome)

            gaps_identified = state.get("gaps_identified")
            score_maturidade = calcular_score(gaps_identified)

            client.table("startups").update({
                "classification": state.get("classification"),
                "classification_confidence": state.get("classification_confidence"),
                "gaps_identified": gaps_identified,
                "recommendations": state.get("recommendations"),
                "briefing": state.get("briefing"),
                "score_maturidade": score_maturidade,
                "analysis_status": "analisada",
                "analyzed_at": datetime.utcnow().isoformat(),
            }).eq("nome", nome).execute()

            print(
                f"  ✓ {nome} — {state.get('classification')} ({score_maturidade['total']}/100)",
                flush=True,
            )
            sucessos += 1

        except Exception as e:
            client.table("startups").update({"analysis_status": "falhou"}).eq("nome", nome).execute()
            print(f"  ✗ {nome} — ERRO: {e}", flush=True)
            falhas += 1

    print(flush=True)
    print(f"Batch concluído: {sucessos} analisadas, {falhas} falhas", flush=True)


if __name__ == "__main__":
    main()
