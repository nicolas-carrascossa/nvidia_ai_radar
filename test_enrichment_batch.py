#!/usr/bin/env python3
"""
Pipeline completo: discovery -> save_discovery -> get_pending_enrichment -> enrich -> update_enrichment_status.
Roda: python test_enrichment_batch.py
"""

import logging

from db.supabase_client import get_pending_enrichment, save_discovery, update_enrichment_status
from scrapers.enricher import enrich
from scrapers.filter import has_ai_signal
from scrapers.sources.ace_ventures import AceVenturesScraper
from scrapers.sources.darwin_startups import DarwinStartupsScraper
from scrapers.sources.startups_com_br import StartupsComBrScraper
from scrapers.sources.wow_aceleradora import WowAceleradoraScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

SOURCES = [
    lambda: StartupsComBrScraper().discover(limit=10),
    lambda: WowAceleradoraScraper().discover(),
    lambda: DarwinStartupsScraper().discover(),
    lambda: AceVenturesScraper().discover(),
]


def main() -> None:
    # ------------------------------------------------------------------ #
    # 1. Discovery + filtro + save_discovery
    # ------------------------------------------------------------------ #
    total_descoberto_rodada = 0
    total_novo = 0

    for discover_fn in SOURCES:
        try:
            discovered = discover_fn()
        except Exception as e:
            logging.error("Erro em discover: %s", e)
            continue

        filtered = [s for s in discovered if has_ai_signal(s.get("snippet", ""))]
        total_descoberto_rodada += len(filtered)

        for startup in filtered:
            if save_discovery(startup):
                total_novo += 1

    print(f"\nDiscovery esta rodada (com sinal IA): {total_descoberto_rodada}")
    print(f"Novas salvas no banco               : {total_novo}\n")

    # ------------------------------------------------------------------ #
    # 2. Enriquecer pendentes
    # ------------------------------------------------------------------ #
    pending = get_pending_enrichment()
    print(f"Pendentes para enrichment           : {len(pending)}\n")

    contagem = {"enriquecida": 0, "parcial": 0, "falhou": 0}

    for startup in pending:
        nome = startup.get("nome", "?")
        fonte = startup.get("fonte_origem", "?")
        print("=" * 60)
        print(f"Startup: {nome}  [{fonte}]")

        try:
            result = enrich(startup)
        except Exception as e:
            logging.error("Erro inesperado em enrich(%s): %s", nome, e)
            result = {
                "nome": nome,
                "fonte_origem": fonte,
                "url_origem": startup.get("url_origem", ""),
                "status": "falhou",
            }

        final_status = result.get("status", "falhou")
        tecnologias = result.get("tecnologias_ia") or []

        print(f"  Status  : {final_status}")
        print(f"  Site    : {result.get('site') or 'nao encontrado'}")
        print(f"  Setor   : {result.get('setor') or 'None'}")
        print(f"  Tipo IA : {result.get('tipo_ia') or 'None'}")
        print(f"  Tecnol. : {', '.join(tecnologias) if tecnologias else 'None'}")

        saved = update_enrichment_status(
            nome=nome,
            fonte_origem=fonte,
            status=final_status,
            dados=result,
        )
        if not saved:
            print("  [ERRO] Falha ao atualizar no banco")

        contagem[final_status] = contagem.get(final_status, 0) + 1

    # ------------------------------------------------------------------ #
    # 3. Resumo
    # ------------------------------------------------------------------ #
    print(f"\n{'=' * 60}")
    print("RESUMO")
    print(f"  Discovery esta rodada (com sinal IA): {total_descoberto_rodada}")
    print(f"  Novas salvas no banco               : {total_novo}")
    print(f"  Pendentes processadas               : {len(pending)}")
    print(f"  -> enriquecida                      : {contagem['enriquecida']}")
    print(f"  -> parcial                          : {contagem['parcial']}")
    print(f"  -> falhou                           : {contagem['falhou']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
