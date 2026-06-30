from abc import ABC, abstractmethod


class BaseScraper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> dict:
        """
        Scrape a URL and return structured data.

        Returns:
            dict with keys:
                url     (str) - the scraped URL
                title   (str) - page title
                content (str) - clean markdown text
                source  (str) - scraper identifier
        """
