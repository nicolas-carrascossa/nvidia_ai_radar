#!/usr/bin/env python3
"""Validate vector search quality against the Qdrant collection.

Run from repo root:  python rag/scripts/04_test_search.py
Or from rag/:        python scripts/04_test_search.py
"""
import os
import sys
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAG_ROOT))

from dotenv import load_dotenv

load_dotenv(RAG_ROOT.parent / ".env")
load_dotenv(RAG_ROOT / ".env", override=True)

import cohere
from qdrant_client import QdrantClient

COLLECTION_NAME = "nvidia_tech_knowledge"
EMBED_MODEL = "embed-multilingual-v3.0"
TOP_K = 5
SNIPPET_LEN = 150

QUERIES = [
    "Como otimizar latência de inferência de LLMs?",
    "Quais tecnologias NVIDIA ajudam com processamento de voz?",
    "O que é o programa Inception da NVIDIA?",
    "Como acelerar processamento de dados tabulares com GPU?",
    "O que é NeMo Guardrails e para que serve?",
]


def main() -> None:
    cohere_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    missing = [
        k for k, v in {
            "COHERE_API_KEY": cohere_key,
            "QDRANT_URL": qdrant_url,
            "QDRANT_API_KEY": qdrant_key,
        }.items() if not v
    ]
    if missing:
        raise ValueError(f"Missing env vars: {', '.join(missing)}")

    co = cohere.Client(api_key=cohere_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)

    for query in QUERIES:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        response = co.embed(
            texts=[query],
            model=EMBED_MODEL,
            input_type="search_query",  # diferente de "search_document" usado na indexação
        )
        vector = list(response.embeddings)[0]

        results = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=TOP_K,
            with_payload=True,
        )
        hits = results.points

        if not hits:
            print("  (nenhum resultado)")
            continue

        for i, hit in enumerate(hits, 1):
            payload = hit.payload or {}
            tecnologia = payload.get("tecnologia", "?")
            url = payload.get("url", "?")
            texto = payload.get("texto", "")
            snippet = texto[:SNIPPET_LEN].replace("\n", " ")
            if len(texto) > SNIPPET_LEN:
                snippet += "..."

            print(f"\n  [{i}] score={hit.score:.4f}  tecnologia={tecnologia}")
            print(f"      url: {url}")
            print(f"      \"{snippet}\"")

    print("\n" + "=" * 70)
    print("Busca concluída.")


if __name__ == "__main__":
    main()
