#!/usr/bin/env python3
"""Embed chunks with Cohere and upload to Qdrant Cloud.

Run from repo root:  python rag/scripts/03_embed_upload.py
Or from rag/:        python scripts/03_embed_upload.py
"""
import json
import os
import sys
import time
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAG_ROOT))

from dotenv import load_dotenv

load_dotenv(RAG_ROOT.parent / ".env")   # raiz do repo (chaves compartilhadas)
load_dotenv(RAG_ROOT / ".env", override=True)  # rag/.env sobrescreve se existir

import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

CHUNKS_FILE = RAG_ROOT / "data" / "chunks" / "chunks.json"
COLLECTION_NAME = "nvidia_tech_knowledge"
VECTOR_SIZE = 1024  # embed-multilingual-v3.0 produces 1024-dim vectors
BATCH_SIZE = 25
BATCH_PAUSE = 3       # seconds between successful batches (rate limit headroom)
EMBED_MODEL = "embed-multilingual-v3.0"
_RETRY_DELAYS = [10, 20, 40, 60, 60]  # backoff schedule for embed retries


def _embed_with_retry(client: cohere.Client, texts: list[str]) -> list[list[float]]:
    for attempt, delay in enumerate(_RETRY_DELAYS):
        try:
            response = client.embed(
                texts=texts,
                model=EMBED_MODEL,
                input_type="search_document",
            )
            return list(response.embeddings)
        except Exception as e:
            if attempt == len(_RETRY_DELAYS) - 1:
                raise
            print(f"  Embed attempt {attempt + 1}/{len(_RETRY_DELAYS)} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
    return []  # unreachable, satisfies type checker


def main() -> None:
    cohere_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    missing = [k for k, v in {"COHERE_API_KEY": cohere_key, "QDRANT_URL": qdrant_url, "QDRANT_API_KEY": qdrant_key}.items() if not v]
    if missing:
        raise ValueError(f"Missing required env vars in rag/.env: {', '.join(missing)}")

    if not CHUNKS_FILE.exists():
        print(f"chunks.json not found at {CHUNKS_FILE}. Run 02_chunk.py first.")
        sys.exit(1)

    co = cohere.Client(api_key=cohere_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)

    if qdrant.collection_exists(COLLECTION_NAME):
        print(f"Collection existente encontrada, deletando para reconstruir do zero...")
        qdrant.delete_collection(COLLECTION_NAME)

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print("Collection recriada vazia.")

    chunks: list[dict] = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    total = len(chunks)
    num_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"Uploading {total} chunks in {num_batches} batches of up to {BATCH_SIZE} (pause {BATCH_PAUSE}s between batches)...\n")

    points_sent = 0
    for batch_idx in range(num_batches):
        batch = chunks[batch_idx * BATCH_SIZE : (batch_idx + 1) * BATCH_SIZE]
        texts = [c["texto"] for c in batch]

        try:
            vectors = _embed_with_retry(co, texts)
        except Exception as e:
            print(f"\nFailed after all retries on batch {batch_idx + 1}/{num_batches}.")
            print(f"Points successfully sent before failure: {points_sent}/{total}")
            raise

        points = [
            PointStruct(
                id=c["id"],
                vector=vec,
                payload={
                    "texto": c["texto"],
                    "url": c["url"],
                    "tecnologia": c["tecnologia"],
                    "titulo": c["titulo"],
                },
            )
            for c, vec in zip(batch, vectors)
        ]

        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
        points_sent += len(batch)
        print(f"Batch {batch_idx + 1}/{num_batches} enviado ({points_sent}/{total} pontos no total)")

        if batch_idx < num_batches - 1:
            time.sleep(BATCH_PAUSE)

    count = qdrant.count(collection_name=COLLECTION_NAME).count
    print("\n" + "=" * 60)
    print(f"Done. Total points in collection '{COLLECTION_NAME}': {count}")


if __name__ == "__main__":
    main()
