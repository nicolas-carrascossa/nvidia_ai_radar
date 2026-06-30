#!/usr/bin/env python3
"""RAG generation with citations — final pipeline step.

Reuses hybrid search + reranking from 05_hybrid_rerank.py (imported via
importlib because the filename starts with a digit).

Run from repo root:  python rag/scripts/06_generate.py
Or from rag/:        python scripts/06_generate.py
"""
import importlib.util
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

# ── import pipeline functions from 05_hybrid_rerank.py ───────────────────────
# importlib is required because the filename starts with a digit.
_spec = importlib.util.spec_from_file_location(
    "hybrid_rerank", SCRIPTS_DIR / "05_hybrid_rerank.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

carregar_corpus_bm25 = _mod.carregar_corpus_bm25
busca_vetorial = _mod.busca_vetorial
busca_bm25 = _mod.busca_bm25
combinar_hibrido = _mod.combinar_hibrido
rerank = _mod.rerank

# ── remaining imports (after env is loaded) ───────────────────────────────────
import cohere
from openai import OpenAI
from qdrant_client import QdrantClient

GENERATION_MODEL = "gpt-4o-mini"
_OAI_RETRY_DELAYS = [5, 10, 20]

QUERIES = [
    "Como otimizar latencia de inferencia de LLMs?",
    "Quais tecnologias NVIDIA ajudam com processamento de voz?",
    "O que e o programa Inception da NVIDIA?",
    "Como acelerar processamento de dados tabulares com GPU?",
    "O que e NeMo Guardrails e para que serve?",
]

_SYSTEM_PROMPT = """\
You are a technical assistant specialized in NVIDIA technologies.
Answer the user's question using ONLY the information present in the numbered \
excerpts provided. Do not add, infer, or invent any detail not explicitly \
stated in those excerpts.

Citation rule: cite each statement using [N], where N is the number of the \
excerpt the information came from, exactly as numbered above. Use ONLY the \
numbers provided — never invent a URL, never use a number outside the range \
given, and never cite something not present in the numbered excerpts. \
If multiple excerpts support the same statement, list all relevant numbers, \
e.g. [1][3].

URL leakage rule: the excerpts may contain hyperlinks to other pages inside \
the text itself (e.g. blog posts, external documentation, GitHub links). \
NEVER cite or mention those internal URLs as a source in your answer — your \
only valid citation is the excerpt number [N], never a URL extracted from \
inside the text.

If the excerpts do not contain sufficient information to answer the question, \
say so clearly instead of guessing.
Respond in the same language as the user's question.\
"""


# ── citation validator ────────────────────────────────────────────────────────

def _validar_citacoes(answer: str, top_n: int) -> list[str]:
    """Return warning strings for out-of-range [N] citations or leaked URLs."""
    warnings = []

    cited = [int(n) for n in re.findall(r'\[(\d+)\]', answer)]
    invalid_nums = sorted({n for n in cited if n < 1 or n > top_n})
    if invalid_nums:
        warnings.append(
            f"Numeros de citacao fora do intervalo [1-{top_n}]: {invalid_nums}"
        )

    leaked_urls = re.findall(r'https?://\S+', answer)
    if leaked_urls:
        warnings.append(
            f"URLs soltas na resposta (possivel vazamento): {leaked_urls}"
        )

    return warnings


# ── OpenAI call with simple retry ─────────────────────────────────────────────

def _chat_with_retry(oai: OpenAI, messages: list[dict]) -> str:
    for attempt, delay in enumerate(_OAI_RETRY_DELAYS):
        try:
            resp = oai.chat.completions.create(
                model=GENERATION_MODEL,
                messages=messages,
                temperature=0,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            if attempt == len(_OAI_RETRY_DELAYS) - 1:
                raise
            print(f"  OpenAI attempt {attempt + 1}/{len(_OAI_RETRY_DELAYS)} failed: {e}. "
                  f"Retrying in {delay}s...")
            time.sleep(delay)
    return ""  # unreachable


# ── core generation function ──────────────────────────────────────────────────

def responder(
    query: str,
    co: cohere.Client,
    qdrant: QdrantClient,
    oai: OpenAI,
    bm25,
    metadados: list[dict],
    top_n: int = 5,
) -> tuple[str, list[dict]]:
    """Run the full pipeline and return (generated_answer, chunks_used)."""
    vet = busca_vetorial(query, co, qdrant, top_k=10)
    bm25_res = busca_bm25(query, bm25, metadados, top_k=10)
    combinados = combinar_hibrido(vet, bm25_res)

    if not combinados:
        return "Nenhum trecho relevante encontrado na base de conhecimento.", []

    chunks = rerank(query, combinados, co, top_n=top_n)

    excerpts = "\n\n".join(
        f"[{i + 1}] Tecnologia: {c['tecnologia']}\n"
        f"URL: {c['url']}\n"
        f"Trecho:\n{c['texto']}"
        for i, c in enumerate(chunks)
    )

    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Pergunta: {query}\n\nTrechos de referencia:\n{excerpts}",
        },
    ]

    answer = _chat_with_retry(oai, messages)
    return answer, chunks


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

    for query in QUERIES:
        print("\n" + "=" * 72)
        print(f"PERGUNTA: {query}")
        print("=" * 72)

        answer, chunks = responder(query, co, qdrant, oai, bm25, metadados, top_n=5)

        print("\nRESPOSTA:\n")
        print(answer)

        warnings = _validar_citacoes(answer, top_n=5)
        if warnings:
            print("\n*** POSSIVEL CITACAO INVALIDA DETECTADA ***")
            for w in warnings:
                print(f"  {w}")

        print("\nFONTES USADAS:")
        for i, c in enumerate(chunks, 1):
            print(f"  [{i}] {c['tecnologia']} — {c['url']}")

    print("\n" + "=" * 72)
    print("Concluido.")


if __name__ == "__main__":
    main()
