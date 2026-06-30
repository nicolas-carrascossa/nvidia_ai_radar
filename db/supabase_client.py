import logging
import re
from datetime import datetime, timezone

from supabase import create_client

from config.settings import settings

logger = logging.getLogger(__name__)

_TABLE = "startups"
_CONFLICT_KEY = "nome,fonte_origem"


def normalize_name(nome: str) -> str:
    """Lowercase, strip, remove non-alphanumeric chars. e.g. 'N3urons!' -> 'n3urons'"""
    text = nome.lower().strip()
    return re.sub(r"[^a-z0-9]", "", text)


def save_discovery(startup: dict) -> bool:
    """Insert a newly discovered startup with status='descoberta'. Skips if already exists."""
    payload = {
        "nome": startup.get("nome", ""),
        "fonte_origem": startup.get("fonte_origem", ""),
        "url_origem": startup.get("url_origem", ""),
        "snippet": startup.get("snippet") or None,
        "status": "descoberta",
    }
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        result = client.table(_TABLE).upsert(
            payload, on_conflict=_CONFLICT_KEY, ignore_duplicates=True
        ).execute()
        inserted = bool(result.data)
        if inserted:
            logger.info("Discovery salva: %s", payload["nome"])
        return inserted
    except Exception as e:
        logger.error("Erro ao salvar discovery '%s': %s", startup.get("nome", "?"), e)
        return False


def get_pending_enrichment() -> list[dict]:
    """Return all startups with status='descoberta', ready to be enriched."""
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        result = client.table(_TABLE).select("*").eq("status", "descoberta").execute()
        return result.data or []
    except Exception as e:
        logger.error("Erro ao buscar pendentes de enrichment: %s", e)
        return []


def update_enrichment_status(nome: str, fonte_origem: str, status: str, dados: dict) -> bool:
    """Update enrichment fields + status + data_enrichment for an existing row."""
    _SKIP = {
        "nome", "fonte_origem", "url_origem", "status",
        "data_descoberta", "data_enrichment", "snippet",
    }
    payload = {k: v for k, v in dados.items() if k not in _SKIP}
    payload["status"] = status
    payload["data_enrichment"] = datetime.now(timezone.utc).isoformat()
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        client.table(_TABLE).update(payload).eq("nome", nome).eq("fonte_origem", fonte_origem).execute()
        logger.info("Enrichment atualizado: %s -> %s", nome, status)
        return True
    except Exception as e:
        logger.error("Erro ao atualizar enrichment de '%s': %s", nome, e)
        return False


def save_startup(startup: dict) -> bool:
    """Upsert an enriched startup record into Supabase, keyed by (nome, fonte_origem)."""
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        client.table(_TABLE).upsert(startup, on_conflict=_CONFLICT_KEY).execute()
        logger.info("Salvo no Supabase: %s", startup.get("nome"))
        return True
    except Exception as e:
        logger.error("Erro ao salvar '%s' no Supabase: %s", startup.get("nome", "?"), e)
        return False


def seed_sources() -> None:
    """Upsert known scraping sources into the sources table."""
    _SOURCES = [
        ("wow_aceleradora", "https://wow.ac/portfolio/", "portfolio", "mensal"),
        ("darwin_startups", "https://www.darwinstartups.com/startups/", "portfolio", "mensal"),
        ("ace_ventures", "https://aceventures.com.br/portfolio/", "portfolio", "mensal"),
    ]
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        for nome, url, tipo, frequencia in _SOURCES:
            client.table("sources").upsert(
                {"nome": nome, "url": url, "tipo": tipo, "frequencia": frequencia},
                on_conflict="nome",
            ).execute()
            logger.info("Fonte registrada: %s", nome)
    except Exception as e:
        logger.error("Erro ao registrar fontes: %s", e)


def update_source_sync(nome: str) -> None:
    """Update ultima_sync = now() for the given source."""
    try:
        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        client.table("sources").update({"ultima_sync": "now()"}).eq("nome", nome).execute()
        logger.info("ultima_sync atualizada para fonte: %s", nome)
    except Exception as e:
        logger.error("Erro ao atualizar ultima_sync para '%s': %s", nome, e)
