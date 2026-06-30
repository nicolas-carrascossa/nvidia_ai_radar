import json

from openai import OpenAI

from config.settings import settings
from scrapers.base import BaseScraper
from scrapers.firecrawl_scraper import FirecrawlScraper

_SEARCH_QUERY = "startup inteligência artificial Brasil site:startups.com.br"
_MODEL = "gpt-4o-mini"
_SNIPPET_MAX_CHARS = 1500

_SYSTEM_PROMPT = (
    "Você é um assistente especializado em identificar startups brasileiras. "
    "Responda sempre com JSON válido, sem texto adicional."
)

_USER_PROMPT = """\
Analise o texto abaixo e extraia informações sobre a startup de tecnologia mencionada.

Texto:
{snippet}

Retorne um JSON com exatamente estes campos:
- "nome": nome da startup (string, ou null se não encontrar)
- "site_oficial": URL do site oficial da startup (string, ou null se não encontrar)

Se o texto mencionar várias startups, extraia apenas a principal ou mais relevante.
"""


class StartupsComBrScraper(BaseScraper):
    def __init__(self) -> None:
        self._firecrawl = FirecrawlScraper()
        self._openai = OpenAI(api_key=settings.openai_api_key)

    # --- BaseScraper contract ---

    def scrape(self, url: str) -> dict:
        result = self._firecrawl.scrape(url)
        return {
            "url": url,
            "title": "",
            "content": result["markdown"] if result else "",
            "source": "startups.com.br",
        }

    # --- Discovery ---

    def discover(self, limit: int = 10) -> list[dict]:
        """
        Search startups.com.br for AI startups and return structured records.

        Each record:
            nome        (str)       – startup name extracted by LLM
            site        (str|None)  – official website or None
            fonte_origem (str)      – always "startups.com.br"
            url_origem  (str)       – source article URL
            snippet     (str)       – raw text used for extraction
        """
        search_results = self._firecrawl.search(_SEARCH_QUERY, limit=limit)
        discovered = []

        for item in search_results:
            if not self._is_article_url(item.get("url", "")):
                continue
            record = self._extract_startup(item)
            if record is not None:
                discovered.append(record)

        return discovered

    @staticmethod
    def _is_article_url(url: str) -> bool:
        """Return True if the URL looks like an article (not a taxonomy/nav page)."""
        _EXCLUDED = ["/autor/", "/author/", "/tag/", "/categoria/", "/category/", "/page/", "/feed/"]
        return not any(pattern in url for pattern in _EXCLUDED)

    def _extract_startup(self, item: dict) -> dict | None:
        snippet = (item.get("markdown") or "")[:_SNIPPET_MAX_CHARS]
        url_origem = item.get("url", "")

        try:
            response = self._openai.chat.completions.create(
                model=_MODEL,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": _USER_PROMPT.format(snippet=snippet)},
                ],
            )
            data = json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"[StartupsComBrScraper] erro LLM em {url_origem}: {e}")
            return None

        nome = (data.get("nome") or "").strip()
        if not nome:
            return None

        return {
            "nome": nome,
            "site": data.get("site_oficial") or None,
            "fonte_origem": "startups.com.br",
            "url_origem": url_origem,
            "snippet": snippet,
        }
