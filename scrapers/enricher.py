import json
import logging
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from openai import OpenAI

from config.settings import settings
from scrapers.firecrawl_scraper import FirecrawlScraper

logger = logging.getLogger(__name__)

_MODEL = "gpt-4o-mini"
_HTTP_TIMEOUT = 8
_ARTICLE_MAX_CHARS = 3000
_SITE_MAX_CHARS = 3000

# Fontes cujo url_origem é a página de portfólio inteira (não um artigo específico)
_PORTFOLIO_SOURCES = {"wow_aceleradora", "darwin_startups", "ace_ventures"}

_BLOCKED_SEARCH_DOMAINS = {
    "linkedin.com", "youtube.com", "instagram.com",
    "facebook.com", "twitter.com", "x.com",
}

# --------------------------------------------------------------------------- #
# Prompts
# --------------------------------------------------------------------------- #

_SITE_EXTRACTION_SYSTEM = (
    "Você é um assistente especializado em identificar startups brasileiras. "
    "Responda APENAS com JSON válido, sem markdown, sem texto adicional."
)

_SITE_EXTRACTION_USER = """\
Leia o texto abaixo, que é um artigo sobre startups de tecnologia, e identifique \
o site oficial da startup chamada "{nome}".

Texto do artigo:
{article}

Retorne um JSON com exatamente este campo:
- "site_oficial": URL completa do site oficial da startup (string com http/https, ou null se não encontrar)
"""

_FULL_EXTRACTION_SYSTEM = (
    "Você é um analista especializado em startups de inteligência artificial brasileiras. "
    "Responda APENAS com JSON válido, sem markdown, sem texto adicional. "
    "Nunca invente dados — se uma informação não estiver no texto, use null ou lista vazia."
)

_FULL_EXTRACTION_USER = """\
Analise os textos abaixo sobre a startup "{nome}" e preencha o JSON de perfil completo.

--- ARTIGO DE ORIGEM ---
{article}

--- SITE OFICIAL (pode estar vazio) ---
{site_content}

Retorne um JSON com exatamente estes campos:
- "descricao": descrição resumida do que a startup faz (string, ou null)
- "setor": setor de atuação, ex: "saúde", "educação", "finanças", "jurídico" (string, ou null)
- "modelo_negocio": ex: "B2B SaaS", "B2C", "marketplace" (string, ou null)
- "tecnologias_ia": lista de tecnologias de IA usadas, ex: ["LLM", "visão computacional"] (lista de strings, pode ser vazia)
- "tipo_ia": classifique como "AI-native" (IA é o produto principal), "AI-enabled" (IA é funcionalidade adicional) ou "Non-AI" (não usa IA de forma significativa)
- "founders": lista com nomes dos fundadores mencionados (lista de strings, pode ser vazia)
- "funding": rodada ou valor de investimento mencionado, ex: "Série A - R$ 10M" (string, ou null)
- "clientes_mencionados": lista de clientes ou parceiros citados (lista de strings, pode ser vazia)
"""


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _call_llm(system: str, user: str) -> dict:
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return json.loads(response.choices[0].message.content)


def _search_article_cascade(scraper: FirecrawlScraper, nome: str) -> str | None:
    """
    Para fontes de portfólio, busca um artigo específico sobre a startup.
    Retorna o primeiro markdown útil encontrado, ou None se tudo falhar.
    """
    results = scraper.search(f"{nome} startup Brasil", limit=5)
    for result in results:
        url = result.get("url", "")
        netloc = urlparse(url).netloc.lower().removeprefix("www.")
        if any(blocked in netloc for blocked in _BLOCKED_SEARCH_DOMAINS):
            logger.debug("Pulando domínio bloqueado na busca: %s", url)
            continue
        scraped = scraper.scrape(url)
        if scraped and len(scraped.get("markdown", "")) > 200:
            logger.info("Artigo encontrado via busca para %s: %s", nome, url)
            return scraped["markdown"][:_ARTICLE_MAX_CHARS]
        logger.debug("Scrape sem conteúdo útil para %s em %s", nome, url)
    return None


def _validate_url(url: str) -> bool:
    """Return True if the URL responds with a non-error HTTP status."""
    try:
        r = requests.get(url, timeout=_HTTP_TIMEOUT, allow_redirects=True)
        return r.status_code < 500
    except Exception:
        return False


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def enrich(startup: dict) -> dict:
    """
    Enrich a discovery record with structured startup data.

    Steps:
        1. Acquire article context (cascade search for portfolio sources, direct scrape otherwise).
        2. LLM: extract official site from the article.
        3. HTTP validate the site URL (skip, not discard, on failure).
        4. If valid, scrape the official site.
        5. LLM: extract full profile from combined content.

    Always returns a dict with at least {nome, fonte_origem, url_origem, status}.
    Status values: 'enriquecida' | 'parcial' | 'falhou'
    - 'falhou': sem conteúdo processável OU LLM do passo 5 falhou
    - 'parcial': passo 5 completou mas faltou site, descricao ou setor
    - 'enriquecida': site + descricao + setor todos presentes
    """
    nome = startup.get("nome", "")
    url_origem = startup.get("url_origem", "")
    fonte_origem = startup.get("fonte_origem", "")

    logger.info("Iniciando enrichment: %s (%s)", nome, url_origem)

    scraper = FirecrawlScraper()

    # ------------------------------------------------------------------ #
    # 1. Acquire article context
    # ------------------------------------------------------------------ #
    if fonte_origem in _PORTFOLIO_SOURCES:
        # url_origem é a página de portfólio inteira — buscar artigo específico
        article_text = _search_article_cascade(scraper, nome) or startup.get("snippet", "")
        logger.info("Contexto via busca para %s: %d chars", nome, len(article_text))
    else:
        try:
            article_result = scraper.scrape(url_origem)
            article_text = article_result["markdown"][:_ARTICLE_MAX_CHARS] if article_result else startup.get("snippet", "")
        except Exception as e:
            logger.error("Erro ao fazer scrape do artigo %s: %s", url_origem, e)
            article_text = startup.get("snippet", "")

    if not article_text:
        logger.warning("Sem conteúdo para %s — descartando.", nome)
        return {"nome": nome, "fonte_origem": fonte_origem, "url_origem": url_origem, "status": "falhou"}

    # ------------------------------------------------------------------ #
    # 2. Extract official site from article
    # ------------------------------------------------------------------ #
    site: str | None = startup.get("site") or None

    if not site:
        try:
            extraction = _call_llm(
                system=_SITE_EXTRACTION_SYSTEM,
                user=_SITE_EXTRACTION_USER.format(nome=nome, article=article_text),
            )
            site = extraction.get("site_oficial") or None
            logger.info("Site extraído para %s: %s", nome, site)
        except Exception as e:
            logger.error("Erro ao extrair site para %s: %s", nome, e)

        if site and urlparse(site).netloc == urlparse(url_origem).netloc:
            logger.warning("Site extraído é o mesmo domínio do artigo, descartando: %s", site)
            site = None

    # ------------------------------------------------------------------ #
    # 3. Validate site URL via HTTP GET
    # ------------------------------------------------------------------ #
    site_content = ""

    if site:
        if _validate_url(site):
            logger.info("URL válida: %s", site)

            # ----------------------------------------------------------#
            # 4. Scrape official site
            # ----------------------------------------------------------#
            try:
                site_result = scraper.scrape(site)
                site_content = site_result["markdown"][:_SITE_MAX_CHARS] if site_result else ""
            except Exception as e:
                logger.error("Erro ao fazer scrape do site %s: %s", site, e)
        else:
            logger.warning("URL não resolveu, continuando sem site: %s", site)
            site = None

    # ------------------------------------------------------------------ #
    # 5. Full profile extraction
    # ------------------------------------------------------------------ #
    try:
        profile = _call_llm(
            system=_FULL_EXTRACTION_SYSTEM,
            user=_FULL_EXTRACTION_USER.format(
                nome=nome,
                article=article_text,
                site_content=site_content or "(não disponível)",
            ),
        )
    except Exception as e:
        logger.error("Erro na extração de perfil para %s: %s", nome, e)
        return {"nome": nome, "fonte_origem": fonte_origem, "url_origem": url_origem, "status": "falhou"}

    enrich_status = (
        "enriquecida"
        if (site and profile.get("descricao") and profile.get("setor"))
        else "parcial"
    )

    return {
        "nome": nome,
        "site": site,
        "descricao": profile.get("descricao") or None,
        "setor": profile.get("setor") or None,
        "modelo_negocio": profile.get("modelo_negocio") or None,
        "tecnologias_ia": profile.get("tecnologias_ia") or [],
        "tipo_ia": profile.get("tipo_ia") or None,
        "founders": profile.get("founders") or [],
        "funding": profile.get("funding") or None,
        "clientes_mencionados": profile.get("clientes_mencionados") or [],
        "fonte_origem": fonte_origem,
        "url_origem": url_origem,
        "status": enrich_status,
        "data_coleta": datetime.now(timezone.utc).isoformat(),
    }
