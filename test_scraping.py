#!/usr/bin/env python3
"""
Entregável 1 – teste de scraping.
Dado o nome de uma startup, busca o site oficial e imprime o texto extraído.
"""

from scrapers.firecrawl_scraper import FirecrawlScraper


def main(startup_name: str = "Nubank") -> None:
    scraper = FirecrawlScraper()

    # 1. Busca o site oficial via Firecrawl Search
    print(f"[1/2] Buscando '{startup_name}'...")
    results = scraper.search(f"{startup_name} startup fintech Brasil site oficial", limit=5)

    if not results:
        print("Nenhum resultado encontrado.")
        return

    # Prefere URL que contenha o nome da startup (ex: nubank.com.br)
    slug = startup_name.lower()
    official = next(
        (r for r in results if slug in r.get("url", "").lower()),
        results[0],
    )
    print(f"  -> {official['url']}")

    # 2. Scraping completo da página encontrada
    print(f"\n[2/2] Coletando conteúdo completo...")
    page = scraper.scrape(official["url"])

    print(f"\n{'='*60}")
    print(f"URL   : {page['url']}")
    print(f"Título: {page['title']}")
    print(f"Fonte : {page['source']}")
    print(f"{'='*60}")
    print(page["content"][:2000])
    if len(page["content"]) > 2000:
        print(f"\n... [{len(page['content']) - 2000} caracteres omitidos]")


if __name__ == "__main__":
    main("Nubank")
