#!/usr/bin/env python3
"""LLM-as-judge evaluation of the RAG pipeline.

Measures two things for each of the 5 test queries:
  - Chunk relevance: gpt-4o-mini scores each retrieved chunk 1-5
  - Response quality: gpt-4o-mini scores the generated answer on fidelity and
    completeness (each 1-5)

Results are printed per query and saved to /rag/data/evaluation_results.json.
Imports responder() and supporting functions from 06_generate.py (which in turn
loads 05_hybrid_rerank.py) via importlib.

Run from repo root:  python rag/scripts/07_evaluate.py
Or from rag/:        python scripts/07_evaluate.py
"""
import importlib.util
import json
import os
import re
import sys
import time
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(RAG_ROOT))

from dotenv import load_dotenv

load_dotenv(RAG_ROOT.parent / ".env")
load_dotenv(RAG_ROOT / ".env", override=True)

# ── load 06_generate.py (transitively loads 05_hybrid_rerank.py) ─────────────
_spec = importlib.util.spec_from_file_location("generate", SCRIPTS_DIR / "06_generate.py")
_mod_06 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod_06)

responder = _mod_06.responder
carregar_corpus_bm25 = _mod_06.carregar_corpus_bm25
QUERIES = _mod_06.QUERIES

# ── remaining imports ─────────────────────────────────────────────────────────
import cohere
from openai import OpenAI
from qdrant_client import QdrantClient

EVAL_MODEL = "gpt-4o-mini"
EVAL_RESULTS_FILE = RAG_ROOT / "data" / "evaluation_results.json"
_RETRY_DELAYS = [5, 10, 20]


# ── helpers ───────────────────────────────────────────────────────────────────

def _chat(oai: OpenAI, prompt: str) -> str:
    """Single-turn completion with simple retry."""
    messages = [{"role": "user", "content": prompt}]
    for attempt, delay in enumerate(_RETRY_DELAYS):
        try:
            resp = oai.chat.completions.create(
                model=EVAL_MODEL,
                messages=messages,
                temperature=0,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            if attempt == len(_RETRY_DELAYS) - 1:
                raise
            print(f"    OpenAI attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
    return ""  # unreachable


def _parse_int(pattern: str, text: str) -> int:
    """Extract first integer match for pattern, return 0 on failure."""
    m = re.search(pattern, text)
    return int(m.group(1)) if m else 0


def _parse_str(pattern: str, text: str, raw: str) -> str:
    """Extract first string match for pattern, return parse-error fragment on failure."""
    m = re.search(pattern, text)
    return m.group(1).strip() if m else f"[parse error: {raw[:80]}]"


# ── evaluation functions ──────────────────────────────────────────────────────

def avaliar_relevancia_chunks(
    query: str,
    chunks: list[dict],
    oai: OpenAI,
) -> tuple[list[dict], float]:
    """Score each chunk 1-5 for relevance to the query.

    Returns (per_chunk_results, mean_score).
    """
    results = []

    for chunk in chunks:
        prompt = (
            "You are evaluating a RAG retrieval system.\n\n"
            f"Question: {query}\n\n"
            f"Retrieved excerpt (source: {chunk['tecnologia']}):\n{chunk['texto']}\n\n"
            "How relevant is this excerpt for answering the question?\n"
            "Rate from 1 to 5:\n"
            "  1 = completely irrelevant\n"
            "  2 = slightly related but not helpful\n"
            "  3 = somewhat relevant, partial information\n"
            "  4 = relevant, contains useful information\n"
            "  5 = highly relevant, directly answers the question\n\n"
            "Respond in this exact format (nothing else):\n"
            "NOTA: X | JUSTIFICATIVA: <one short sentence>"
        )

        raw = _chat(oai, prompt)
        nota = _parse_int(r'NOTA:\s*([1-5])', raw)
        justificativa = _parse_str(r'JUSTIFICATIVA:\s*(.+)', raw, raw)

        results.append({
            "tecnologia": chunk["tecnologia"],
            "url": chunk["url"],
            "nota": nota,
            "justificativa": justificativa,
        })

    valid = [r["nota"] for r in results if r["nota"] > 0]
    media = round(sum(valid) / len(valid), 2) if valid else 0.0
    return results, media


def avaliar_resposta(
    query: str,
    resposta: str,
    chunks: list[dict],
    oai: OpenAI,
) -> dict:
    """Score the generated answer on fidelity and completeness (each 1-5)."""
    excerpts = "\n\n".join(
        f"[{i + 1}] ({c['tecnologia']}): {c['texto']}"
        for i, c in enumerate(chunks)
    )

    prompt = (
        "You are evaluating the quality of a RAG-generated response.\n\n"
        f"Question: {query}\n\n"
        f"Reference excerpts available to the model:\n{excerpts}\n\n"
        f"Generated response:\n{resposta}\n\n"
        "Evaluate on two dimensions:\n\n"
        "FIDELIDADE (1-5): Does the response use ONLY information from the excerpts, "
        "without inventing anything?\n"
        "  1 = major hallucinations or invented facts\n"
        "  2 = some invented details\n"
        "  3 = mostly faithful with minor issues\n"
        "  4 = faithful, only uses excerpt information\n"
        "  5 = perfectly faithful, every claim traceable to excerpts\n\n"
        "COMPLETUDE (1-5): Does the response adequately cover what was asked, "
        "given the available excerpts?\n"
        "  1 = ignores most available information\n"
        "  2 = covers little of what was available\n"
        "  3 = covers some of the available information\n"
        "  4 = covers most of what was available\n"
        "  5 = comprehensive coverage of available information\n\n"
        "Respond in this exact format (nothing else):\n"
        "FIDELIDADE: X | COMPLETUDE: Y | JUSTIFICATIVA: <one short sentence>"
    )

    raw = _chat(oai, prompt)
    return {
        "fidelidade": _parse_int(r'FIDELIDADE:\s*([1-5])', raw),
        "completude": _parse_int(r'COMPLETUDE:\s*([1-5])', raw),
        "justificativa": _parse_str(r'JUSTIFICATIVA:\s*(.+)', raw, raw),
    }


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    cohere_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    missing = [
        k for k, v in {
            "COHERE_API_KEY": cohere_key,
            "QDRANT_URL": qdrant_url,
            "QDRANT_API_KEY": qdrant_key,
            "OPENAI_API_KEY": openai_key,
        }.items() if not v
    ]
    if missing:
        raise ValueError(f"Missing env vars: {', '.join(missing)}")

    print("Carregando corpus BM25...")
    bm25, metadados = carregar_corpus_bm25()
    print(f"BM25 indexado: {len(metadados)} chunks.\n")

    co = cohere.Client(api_key=cohere_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)
    oai = OpenAI(api_key=openai_key)

    all_results = []

    for query in QUERIES:
        print("\n" + "=" * 72)
        print(f"AVALIANDO: {query}")
        print("=" * 72)

        print("  [1/3] Gerando resposta...")
        resposta, chunks = responder(query, co, qdrant, oai, bm25, metadados, top_n=5)

        print(f"  [2/3] Avaliando relevancia de {len(chunks)} chunks...")
        rel_chunks, rel_media = avaliar_relevancia_chunks(query, chunks, oai)

        print("  [3/3] Avaliando fidelidade e completude da resposta...")
        aval = avaliar_resposta(query, resposta, chunks, oai)

        print(f"\n  Relevancia media dos chunks : {rel_media:.1f}/5")
        for r in rel_chunks:
            print(f"    [{r['nota']}/5] {r['tecnologia']} — {r['justificativa']}")
        print(f"\n  Fidelidade da resposta      : {aval['fidelidade']}/5")
        print(f"  Completude da resposta      : {aval['completude']}/5")
        print(f"  Justificativa               : {aval['justificativa']}")

        all_results.append({
            "query": query,
            "resposta": resposta,
            "chunks": [{"tecnologia": c["tecnologia"], "url": c["url"]} for c in chunks],
            "relevancia_chunks": rel_chunks,
            "relevancia_media": rel_media,
            "avaliacao_resposta": aval,
        })

    # ── aggregate ─────────────────────────────────────────────────────────────
    n = len(all_results)
    rel_geral = round(sum(r["relevancia_media"] for r in all_results) / n, 2)
    fid_geral = round(sum(r["avaliacao_resposta"]["fidelidade"] for r in all_results) / n, 2)
    comp_geral = round(sum(r["avaliacao_resposta"]["completude"] for r in all_results) / n, 2)

    output = {
        "results": all_results,
        "agregado": {
            "relevancia_media_geral": rel_geral,
            "fidelidade_media": fid_geral,
            "completude_media": comp_geral,
        },
    }

    EVAL_RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    EVAL_RESULTS_FILE.write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n" + "=" * 72)
    print("RESUMO AGREGADO (5 perguntas)")
    print("=" * 72)
    print(f"  Relevancia media dos chunks : {rel_geral:.2f}/5")
    print(f"  Fidelidade media            : {fid_geral:.2f}/5")
    print(f"  Completude media            : {comp_geral:.2f}/5")
    print(f"\n  Resultados salvos em: {EVAL_RESULTS_FILE}")


if __name__ == "__main__":
    main()
