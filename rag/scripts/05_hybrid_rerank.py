#!/usr/bin/env python3
"""Hybrid search (vector + BM25) with Cohere reranking.

Compares results before and after reranking for 5 fixed test queries,
using the same collection and queries as 04_test_search.py.

Run from repo root:  python rag/scripts/05_hybrid_rerank.py
Or from rag/:        python scripts/05_hybrid_rerank.py
"""
import json
import os
import re
import sys
import time
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAG_ROOT))

from dotenv import load_dotenv

load_dotenv(RAG_ROOT.parent / ".env")
load_dotenv(RAG_ROOT / ".env", override=True)

import cohere
from qdrant_client import QdrantClient
from rank_bm25 import BM25Okapi

CHUNKS_FILE = RAG_ROOT / "data" / "chunks" / "chunks.json"
COLLECTION_NAME = "nvidia_tech_knowledge"
EMBED_MODEL = "embed-multilingual-v3.0"
RERANK_MODEL = "rerank-v3.5"
_RETRY_DELAYS = [10, 20, 40, 60, 60]

QUERIES = [
    "Como otimizar latencia de inferencia de LLMs?",
    "Quais tecnologias NVIDIA ajudam com processamento de voz?",
    "O que e o programa Inception da NVIDIA?",
    "Como acelerar processamento de dados tabulares com GPU?",
    "O que e NeMo Guardrails e para que serve?",
]


# ── helpers ───────────────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    return re.findall(r'\b\w+\b', text.lower())


def _with_retry(fn, *args, label: str = "API call", **kwargs):
    """Call fn(*args, **kwargs) with exponential backoff on failure.
    `label` is keyword-only and is NOT forwarded to fn.
    """
    for attempt, delay in enumerate(_RETRY_DELAYS):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if attempt == len(_RETRY_DELAYS) - 1:
                raise
            print(f"  {label} attempt {attempt + 1}/{len(_RETRY_DELAYS)} failed: {e}. "
                  f"Retrying in {delay}s...")
            time.sleep(delay)


def _snippet(text: str, length: int) -> str:
    flat = text.replace("\n", " ")
    return flat[:length] + ("..." if len(flat) > length else "")


# ── core functions ────────────────────────────────────────────────────────────

def carregar_corpus_bm25() -> tuple[BM25Okapi, list[dict]]:
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    tokenized_corpus = [_tokenize(c["texto"]) for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    metadados = [
        {
            "id": c["id"],
            "texto": c["texto"],
            "url": c["url"],
            "tecnologia": c["tecnologia"],
            "titulo": c["titulo"],
        }
        for c in chunks
    ]
    return bm25, metadados


def busca_vetorial(
    query: str,
    co: cohere.Client,
    qdrant: QdrantClient,
    top_k: int = 10,
) -> list[dict]:
    response = _with_retry(
        co.embed,
        texts=[query],
        model=EMBED_MODEL,
        input_type="search_query",
        label="embed (vetorial)",
    )
    vector = list(response.embeddings)[0]

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=top_k,
        with_payload=True,
    )
    output = []
    for hit in results.points:
        p = hit.payload or {}
        output.append({
            "id": str(hit.id),
            "texto": p.get("texto", ""),
            "url": p.get("url", ""),
            "tecnologia": p.get("tecnologia", ""),
            "titulo": p.get("titulo", ""),
            "score_vetorial": hit.score,
            "fonte": "vetorial",
        })
    return output


def busca_bm25(
    query: str,
    bm25: BM25Okapi,
    metadados: list[dict],
    top_k: int = 10,
) -> list[dict]:
    tokenized_query = _tokenize(query)
    scores = bm25.get_scores(tokenized_query)
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    output = []
    for idx in ranked_indices:
        if scores[idx] == 0:
            break  # no BM25 signal for the rest
        m = metadados[idx]
        output.append({
            "id": m["id"],
            "texto": m["texto"],
            "url": m["url"],
            "tecnologia": m["tecnologia"],
            "titulo": m["titulo"],
            "score_bm25": float(scores[idx]),
            "fonte": "bm25",
        })
    return output


def combinar_hibrido(
    resultados_vetorial: list[dict],
    resultados_bm25: list[dict],
) -> list[dict]:
    """Merge and deduplicate by chunk id.

    Chunks present in both lists are marked fonte='hibrido' and carry both
    scores. Order: hibrido first, then vetorial-only, then bm25-only.
    Within each group sorted by the available score descending.
    """
    combined: dict[str, dict] = {}

    for item in resultados_vetorial:
        combined[item["id"]] = item.copy()

    for item in resultados_bm25:
        if item["id"] in combined:
            combined[item["id"]]["fonte"] = "hibrido"
            combined[item["id"]]["score_bm25"] = item["score_bm25"]
        else:
            combined[item["id"]] = item.copy()

    def _sort_key(c: dict) -> tuple:
        if c["fonte"] == "hibrido":
            return (0, -c.get("score_vetorial", 0))
        elif c["fonte"] == "vetorial":
            return (1, -c.get("score_vetorial", 0))
        else:
            return (2, -c.get("score_bm25", 0))

    return sorted(combined.values(), key=_sort_key)


def rerank(
    query: str,
    chunks_combinados: list[dict],
    co: cohere.Client,
    top_n: int = 5,
) -> list[dict]:
    documents = [c["texto"] for c in chunks_combinados]
    response = _with_retry(
        co.rerank,
        model=RERANK_MODEL,
        query=query,
        documents=documents,
        top_n=top_n,
        label="rerank",
    )
    reranked = []
    for result in response.results:
        reranked.append({
            **chunks_combinados[result.index],
            "relevance_score": result.relevance_score,
        })
    return reranked


# ── display helpers ───────────────────────────────────────────────────────────

def _imprimir_pre_rerank(chunks: list[dict]) -> None:
    print("  ANTES DO RERANK:")
    for i, c in enumerate(chunks, 1):
        scores_parts = []
        if "score_vetorial" in c:
            scores_parts.append(f"vec={c['score_vetorial']:.4f}")
        if "score_bm25" in c:
            scores_parts.append(f"bm25={c['score_bm25']:.3f}")
        scores_str = "  ".join(scores_parts)
        print(f"  [{i:2d}] [{c['fonte']:8s}]  {scores_str:30s}  tec={c['tecnologia']}")
        print(f"        \"{_snippet(c['texto'], 100)}\"")


def _imprimir_pos_rerank(reranked: list[dict]) -> None:
    print("  DEPOIS DO RERANK (top 5):")
    for i, c in enumerate(reranked, 1):
        print(f"  [{i}] relevance={c['relevance_score']:.4f}  tec={c['tecnologia']}")
        print(f"      \"{_snippet(c['texto'], 150)}\"")


def _observacao(chunks_pre: list[dict], reranked: list[dict]) -> None:
    if not chunks_pre or not reranked:
        return
    top1_pre = chunks_pre[0]
    top1_pos = reranked[0]

    if top1_pre["id"] == top1_pos["id"]:
        print(f"  Obs: '{top1_pos['tecnologia']}' manteve a posicao #1 apos o rerank.")
        return

    pre_ids = [c["id"] for c in chunks_pre]
    try:
        nova_origem = pre_ids.index(top1_pos["id"]) + 1
    except ValueError:
        nova_origem = "?"

    pos_ids = [c["id"] for c in reranked]
    try:
        destino_antigo = f"caiu para #{pos_ids.index(top1_pre['id']) + 1}"
    except ValueError:
        destino_antigo = f"saiu do top-{len(reranked)}"

    print(
        f"  Obs: '{top1_pre['tecnologia']}' (pre-rerank #1) {destino_antigo}; "
        f"'{top1_pos['tecnologia']}' subiu do #{nova_origem} para o topo."
    )


# ── main ──────────────────────────────────────────────────────────────────────

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

    if not CHUNKS_FILE.exists():
        print(f"chunks.json not found at {CHUNKS_FILE}. Run 02_chunk.py first.")
        sys.exit(1)

    print("Carregando corpus BM25...")
    bm25, metadados = carregar_corpus_bm25()
    print(f"BM25 indexado: {len(metadados)} chunks.\n")

    co = cohere.Client(api_key=cohere_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)

    for query in QUERIES:
        print("\n" + "=" * 72)
        print(f"QUERY: {query}")
        print("=" * 72)

        vet = busca_vetorial(query, co, qdrant, top_k=10)
        bm25_res = busca_bm25(query, bm25, metadados, top_k=10)
        combinados = combinar_hibrido(vet, bm25_res)

        n_hibrido = sum(1 for c in combinados if c["fonte"] == "hibrido")
        print(f"\n  Combinado: {len(combinados)} chunks unicos "
              f"({n_hibrido} aparecem nas duas buscas)\n")

        _imprimir_pre_rerank(combinados)

        if not combinados:
            print("  (sem resultados para reranquear)")
            continue

        print()
        reranked = rerank(query, combinados, co, top_n=5)
        _imprimir_pos_rerank(reranked)

        print()
        _observacao(combinados, reranked)

    print("\n" + "=" * 72)
    print("Concluido.")


if __name__ == "__main__":
    main()
