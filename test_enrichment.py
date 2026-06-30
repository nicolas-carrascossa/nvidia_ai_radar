#!/usr/bin/env python3
"""
Fase 2 – teste do pipeline discovery -> filtro -> enrichment -> Supabase.
Roda: python test_enrichment.py
"""

import logging

from db.supabase_client import save_startup, update_source_sync
from scrapers.enricher import enrich
from scrapers.filter import has_ai_signal
from scrapers.sources.startups_com_br import StartupsComBrScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

_CAMPOS_SIMPLES = ["descricao", "setor", "modelo_negocio", "tipo_ia", "funding"]
_CAMPOS_LISTA = ["tecnologias_ia", "founders", "clientes_mencionados"]


def main() -> None:
    scraper = StartupsComBrScraper()
    discovered = scraper.discover(limit=10)
    filtered = [s for s in discovered if has_ai_signal(s["snippet"])]

    print(f"\nDiscovery: {len(discovered)} encontradas, {len(filtered)} com sinal de IA\n")

    for startup in filtered:
        nome = startup["nome"]
        print("=" * 60)
        print(f"Startup: {nome}")

        enriched = enrich(startup)
        if enriched is None:
            print(f"  -> PULADO (já enriquecido ou sem dados)")
        elif enriched:
            print(f"  -> OK")
        else:
            print(f"  -> FALHOU")

    print("=" * 60)
    update_source_sync("startups_com_br")


if __name__ == "__main__":
    main()
