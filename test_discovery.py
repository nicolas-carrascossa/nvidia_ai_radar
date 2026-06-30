#!/usr/bin/env python3
"""
Entregável 1 – teste do pipeline discovery + filtro de sinal de IA.
Roda: python test_discovery.py
"""

from scrapers.filter import has_ai_signal
from scrapers.sources.startups_com_br import StartupsComBrScraper


def main() -> None:
    print("Iniciando discovery em startups.com.br...\n")

    scraper = StartupsComBrScraper()
    discovered = scraper.discover(limit=10)

    filtered = [s for s in discovered if has_ai_signal(s["snippet"])]

    print(f"Total descoberto   : {len(discovered)}")
    print(f"Com sinal de IA    : {len(filtered)}")

    if not filtered:
        print("\nNenhuma startup passou no filtro de sinal de IA.")
        return

    print("\n" + "=" * 60)
    for s in filtered:
        print(f"Nome       : {s['nome']}")
        print(f"Site       : {s['site'] or '(não encontrado)'}")
        print(f"Url origem : {s['url_origem']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
