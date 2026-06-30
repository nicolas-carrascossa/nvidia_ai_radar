#!/usr/bin/env python3
"""
Teste de discovery multi-fonte: startups.com.br, WOW Aceleradora, Darwin Startups.
Roda: python test_discovery_sources.py
"""

import logging

from db.supabase_client import seed_sources
from scrapers.filter import has_ai_signal
from scrapers.sources.ace_ventures import AceVenturesScraper
from scrapers.sources.darwin_startups import DarwinStartupsScraper
from scrapers.sources.startups_com_br import StartupsComBrScraper
from scrapers.sources.wow_aceleradora import WowAceleradoraScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

SOURCES = [
    ("startups.com.br",  lambda: StartupsComBrScraper().discover(limit=10)),
    ("wow_aceleradora",  lambda: WowAceleradoraScraper().discover()),
    ("darwin_startups",  lambda: DarwinStartupsScraper().discover()),
    ("ace_ventures",     lambda: AceVenturesScraper().discover()),
]


def main() -> None:
    seed_sources()

    total_descoberto = 0
    total_ai = 0

    for fonte, discover_fn in SOURCES:
        print(f"\n{'=' * 60}")
        print(f"Fonte: {fonte}")

        discovered = discover_fn()
        filtered = [s for s in discovered if has_ai_signal(s["snippet"])]

        print(f"  Descobertas : {len(discovered)}")
        print(f"  Com sinal IA: {len(filtered)}")

        for s in filtered:
            print(f"    - {s['nome']}")

        total_descoberto += len(discovered)
        total_ai += len(filtered)

    print(f"\n{'=' * 60}")
    print(f"TOTAL GERAL")
    print(f"  Descobertas : {total_descoberto}")
    print(f"  Com sinal IA: {total_ai}")
    print("=" * 60)


if __name__ == "__main__":
    main()
