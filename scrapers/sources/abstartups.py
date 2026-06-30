from scrapers.firecrawl_scraper import FirecrawlScraper

# ABStartups (Associação Brasileira de Startups) member directory
ABSTARTUPS_LISTING_URL = "https://abstartups.com.br/startupbase/"


class ABStartupsScraper:
    SOURCE = "abstartups"

    def __init__(self) -> None:
        self._scraper = FirecrawlScraper()

    def scrape_listing(self) -> list[dict]:
        """Scrape the ABStartups member directory page."""
        result = self._scraper.scrape(ABSTARTUPS_LISTING_URL)
        if result is None:
            return []
        return [result]

    def search_startup(self, name: str) -> list[dict]:
        """Search ABStartups for a specific startup by name."""
        query = f"{name} startup site:abstartups.com.br"
        results = self._scraper.search(query, limit=3)
        for r in results:
            r["source"] = self.SOURCE
        return results
