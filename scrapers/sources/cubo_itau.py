import json

from openai import OpenAI

from config.settings import settings
from scrapers.base import BaseScraper
from scrapers.firecrawl_scraper import FirecrawlScraper


def _strip_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ```) from LLM output."""
    text = text.strip()
    if text.startswith("```"):
        text = text[text.index("\n") + 1:]
        if text.endswith("```"):
            text = text[: text.rindex("```")].strip()
    return text


_MODEL = "gpt-4o-mini"
_PORTFOLIO_URL = "https://cubo.network/startups"
_FONTE_ORIGEM = "cubo_itau"
_CONTENT_MAX_CHARS = 8000
_MIN_USEFUL_CHARS = 500

_SYSTEM_PROMPT = (
    "Você é um assistente especializado em identificar startups brasileiras. "
    "Responda sempre com JSON válido, sem texto adicional."
)

_USER_PROMPT = """\
Abaixo está o conteúdo de uma página de portfólio de uma aceleradora.
Extraia todas as empresas mencionadas. Para cada uma retorne um JSON
com os campos: nome (string) e snippet (string com a descrição ou
pitch da empresa, máximo 200 caracteres). Retorne apenas um array
JSON válido, sem texto adicional.

Conteúdo:
{content}
"""


class CuboItauScraper(BaseScraper):
    def __init__(self) -> None:
        self._firecrawl = FirecrawlScraper()
        self._openai = OpenAI(api_key=settings.openai_api_key)

    # --- BaseScraper contract ---

    def scrape(self, url: str) -> dict:
        result = self._firecrawl.scrape(url, wait_for=5000)
        return {
            "url": url,
            "title": "",
            "content": result["markdown"] if result else "",
            "source": _FONTE_ORIGEM,
        }

    # --- Discovery ---

    def discover(self) -> list[dict]:
        page = self._firecrawl.scrape(_PORTFOLIO_URL, wait_for=5000)

        markdown = page["markdown"] if page else ""
        print(f"[CuboItauScraper] markdown recebido: {len(markdown)} chars")

        if len(markdown) < _MIN_USEFUL_CHARS:
            print(f"[CuboItauScraper] conteudo insuficiente (< {_MIN_USEFUL_CHARS} chars) — abortando")
            print(f"[CuboItauScraper] conteudo bruto: {repr(markdown[:300])}")
            return []

        content = markdown[:_CONTENT_MAX_CHARS]

        try:
            response = self._openai.chat.completions.create(
                model=_MODEL,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": _USER_PROMPT.format(content=content)},
                ],
            )
            raw = _strip_fences(response.choices[0].message.content or "")
            parsed = json.loads(raw)
            items = parsed if isinstance(parsed, list) else (
                parsed.get("empresas") or parsed.get("startups") or []
            )
        except Exception as e:
            print(f"[CuboItauScraper] erro LLM: {e}")
            return []

        discovered = []
        for item in items:
            try:
                nome = (item.get("nome") or "").strip()
                if not nome:
                    continue
                discovered.append({
                    "nome": nome,
                    "site": None,
                    "fonte_origem": _FONTE_ORIGEM,
                    "url_origem": _PORTFOLIO_URL,
                    "snippet": (item.get("snippet") or "")[:200],
                })
            except Exception as e:
                print(f"[CuboItauScraper] erro ao processar item {item}: {e}")

        return discovered
