from firecrawl import FirecrawlApp

from config.settings import settings

_BOT_CHECK_PHRASE = "Checking your browser"
_MIN_CONTENT_LEN = 200


class FirecrawlScraper:
    def __init__(self) -> None:
        self._app = FirecrawlApp(api_key=settings.firecrawl_api_key)

    def search(self, query: str, limit: int = 3) -> list[dict]:
        """Search via Firecrawl and return list of {url, markdown} dicts.

        Firecrawl v4 search returns SearchData with a .web list of SearchResult
        (fields: url, title, description). There is no per-result markdown at
        this stage; description is used as the markdown proxy for signal detection.
        """
        try:
            data = self._app.search(query, limit=limit)
            items = getattr(data, "web", []) or []
            results = []
            for item in items:
                url = getattr(item, "url", "") or ""
                markdown = getattr(item, "description", "") or getattr(item, "title", "") or ""
                if url:
                    results.append({"url": url, "markdown": markdown})
            return results
        except Exception as e:
            print(f"[FirecrawlScraper.search] erro: {e}")
            return []

    def scrape(self, url: str, *, wait_for: int | None = None, actions: list | None = None) -> dict | None:
        """Scrape a URL and return {url, markdown}, or None if content is unusable.

        Firecrawl v4 uses scrape(url, *, formats=[...]) returning a Document object.
        """
        try:
            kwargs = {"formats": ["markdown"]}
            if wait_for is not None:
                kwargs["wait_for"] = wait_for
            if actions is not None:
                kwargs["actions"] = actions
            doc = self._app.scrape(url, **kwargs)
            markdown = getattr(doc, "markdown", "") or ""

            if len(markdown) < _MIN_CONTENT_LEN or _BOT_CHECK_PHRASE in markdown:
                return None

            return {"url": url, "markdown": markdown}
        except Exception as e:
            print(f"[FirecrawlScraper.scrape] erro em {url}: {e}")
            return None
