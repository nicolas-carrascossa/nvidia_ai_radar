#!/usr/bin/env python3
"""Extract raw content from NVIDIA documentation sources using Firecrawl.

Run from repo root:  python rag/scripts/01_extract.py
Or from rag/:        python scripts/01_extract.py
"""
import os
import re
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAG_ROOT))

from dotenv import load_dotenv
from firecrawl import FirecrawlApp

from sources import SOURCES

load_dotenv(RAG_ROOT.parent / ".env")   # raiz do repo (chaves compartilhadas)
load_dotenv(RAG_ROOT / ".env", override=True)  # rag/.env sobrescreve se existir

RAW_DIR = RAG_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
ERRORS_LOG = RAW_DIR / "_errors.log"

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


def _to_slug(tecnologia: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", tecnologia.lower()).strip("_")


def _scrape_with_retry(app: FirecrawlApp, url: str, max_retries: int = 3, delay: int = 5):
    for attempt in range(max_retries):
        try:
            return app.scrape(url, formats=["markdown"])
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            log.warning(f"  Attempt {attempt + 1}/{max_retries} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)


def main() -> None:
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY not set in rag/.env")

    app = FirecrawlApp(api_key=api_key)

    slug_counts: dict[str, int] = {}
    successes: list[tuple[str, str, str]] = []
    failures: list[tuple[str, str, str]] = []

    for source in SOURCES:
        url = source["url"]
        tecnologia = source["tecnologia"]
        slug = _to_slug(tecnologia)

        slug_counts[slug] = slug_counts.get(slug, 0) + 1
        idx = slug_counts[slug]
        filename = f"{slug}_{idx:02d}.md"
        out_path = RAW_DIR / filename

        log.info(f"[{tecnologia}] {url}")
        log.info(f"  → {filename}")

        try:
            doc = _scrape_with_retry(app, url)
            markdown = getattr(doc, "markdown", "") or ""

            if not markdown:
                raise ValueError("Firecrawl returned empty markdown")

            # Extract title from metadata defensively
            metadata = getattr(doc, "metadata", None) or {}
            if isinstance(metadata, dict):
                titulo = metadata.get("title", "") or ""
            else:
                titulo = getattr(metadata, "title", "") or ""

            # Escape any literal newlines in the front-matter values
            titulo_safe = titulo.replace("\n", " ").replace("\r", "")

            content = (
                f"---\n"
                f"url: {url}\n"
                f"tecnologia: {tecnologia}\n"
                f"titulo: {titulo_safe}\n"
                f"---\n\n"
                f"{markdown}"
            )
            out_path.write_text(content, encoding="utf-8")
            successes.append((tecnologia, url, filename))
            log.info(f"  OK ({len(markdown):,} chars)")

        except Exception as e:
            error_line = f"{datetime.now().isoformat()} | {url} | {e}\n"
            with open(ERRORS_LOG, "a", encoding="utf-8") as f:
                f.write(error_line)
            failures.append((tecnologia, url, str(e)))
            log.error(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print(f"Extracted: {len(successes)} succeeded, {len(failures)} failed.")
    if failures:
        print("\nFailed sources:")
        for tec, url, err in failures:
            print(f"  [{tec}] {url}")
            print(f"    {err}")


if __name__ == "__main__":
    main()
