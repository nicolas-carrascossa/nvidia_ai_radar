#!/usr/bin/env python3
"""Chunk raw markdown files into overlapping segments with metadata.

Run from repo root:  python rag/scripts/02_chunk.py
Or from rag/:        python scripts/02_chunk.py
"""
import json
import sys
import uuid
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAG_ROOT))

from langchain_text_splitters import RecursiveCharacterTextSplitter

RAW_DIR = RAG_ROOT / "data" / "raw"
CLEAN_DIR = RAG_ROOT / "data" / "clean"
CHUNKS_DIR = RAG_ROOT / "data" / "chunks"
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
CHUNKS_FILE = CHUNKS_DIR / "chunks.json"


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the ---/--- front-matter block and return (metadata dict, body)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    header = parts[1].strip()
    body = parts[2].strip()
    meta: dict[str, str] = {}
    for line in header.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            meta[key.strip()] = value.strip()
    return meta, body


def main() -> None:
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",  # same encoding as text-embedding-3-small
        chunk_size=600,
        chunk_overlap=100,
    )

    # Prefer cleaned files; fall back to raw if clean/ doesn't exist yet
    source_dir = CLEAN_DIR if (CLEAN_DIR.exists() and any(CLEAN_DIR.glob("*.md"))) else RAW_DIR
    print(f"Reading from: {source_dir.name}/\n")

    md_files = sorted(p for p in source_dir.glob("*.md") if p.name != "_errors.log")

    if not md_files:
        print(f"No .md files found in {source_dir}. Run 01_extract.py (and optionally 01b_clean.py) first.")
        sys.exit(1)

    all_chunks: list[dict] = []

    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(text)

        url = meta.get("url", "")
        tecnologia = meta.get("tecnologia", "")
        titulo = meta.get("titulo", "")

        chunks = splitter.split_text(body)
        for chunk_text in chunks:
            all_chunks.append(
                {
                    "id": str(uuid.uuid4()),
                    "texto": chunk_text,
                    "url": url,
                    "tecnologia": tecnologia,
                    "titulo": titulo,
                }
            )
        print(f"{md_path.name}: {len(chunks)} chunks")

    CHUNKS_FILE.write_text(
        json.dumps(all_chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n" + "=" * 60)
    print(f"Documents processed : {len(md_files)}")
    print(f"Total chunks        : {len(all_chunks)}")
    if md_files:
        print(f"Average per document: {len(all_chunks) / len(md_files):.1f}")
    print(f"Saved to            : {CHUNKS_FILE}")


if __name__ == "__main__":
    main()
