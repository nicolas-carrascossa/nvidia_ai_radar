#!/usr/bin/env python3
"""Clean raw markdown files extracted by Firecrawl.

Applies conservative structural noise removal (in order):
  1. Image-only lines  ->  removed
  2. "On this page" navigation blocks (anchor-link lists)  ->  removed
  3. Permalink-only lines  ->  removed
  4. Navigational/UI section headers + content until next same-level header  ->  removed
  5. Consecutive blank lines  ->  collapsed to one
  6. Bare link lines with fewer than 5 visible words  ->  removed
  7. Geo/language-selector blocks (NVIDIA country list footer)  ->  removed

When in doubt, content is KEPT. Only clearly structural lines are removed.

Run from repo root:  python rag/scripts/01b_clean.py
Or from rag/:        python scripts/01b_clean.py
"""
import re
import sys
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAG_ROOT))

RAW_DIR = RAG_ROOT / "data" / "raw"
CLEAN_DIR = RAG_ROOT / "data" / "clean"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# ── compiled patterns ─────────────────────────────────────────────────────────

# Line that is ONLY an image markdown, optionally wrapped in a link:
#   ![alt](url)   or   [![alt](img)](link)
_IMAGE_LINE = re.compile(r'^\s*\[?!\[.*?\]\([^)]*\)\]?(?:\([^)]*\))?\s*$')

# Line that is ONLY a bare markdown link (no surrounding text):
#   [visible text](url)
_BARE_LINK_LINE = re.compile(r'^\s*\[([^\]]*)\]\([^)]+\)\s*$')

# Permalink-only line (GitHub docs style):
#   [Permalink](#...)   or   Permalink: [text](url)   or   Permalink ¶
_PERMALINK_LINE = re.compile(
    r'^\s*(?:\[Permalink[^\]]*\]\([^)]*\)|Permalink\s*[:#¶]?\s*)$',
    re.IGNORECASE,
)

# Anchor-only list item — used to detect "On this page" nav blocks:
#   - [Section title](#anchor)
_ANCHOR_LIST_ITEM = re.compile(r'^\s*[-*]\s+\[.*?\]\(#[^)]*\)\s*$')

# "On this page" as a standalone text line (not a header):
#   On this page   or   **On this page**
_ON_THIS_PAGE_LINE = re.compile(r'^\s*\*{0,2}On this page\*{0,2}\s*$', re.IGNORECASE)

# Markdown header
_HEADER = re.compile(r'^(#{1,6})\s+(.*)')

# Navigational/UI section header texts to remove (matched case-insensitively).
# Only include headers that are unambiguously non-content.
_NAV_HEADERS: set[str] = {
    "useful links",
    "update your profile",
    "on this page",
    "cancel accept and play video",
    "accept and play video",
    "quick links",
    "in this page",
    "table of contents",
    "related links",
    "external links",
}

# ── rule 7: geo/language-selector block (NVIDIA country footer) ───────────────

# List item linking to an external URL (not a #anchor):  - [Label](https://...)
_EXT_LINK_ITEM = re.compile(r'^\s*[-*]\s+\[.+?\]\(https?://[^)]+\)\s*$')

# Standalone region headings that appear before country lists
_REGION_HEADER = re.compile(
    r'^\s*(?:Europe|Americas|Asia\s+Pacific|Middle\s+East|Africa|Oceania|'
    r'Latin\s+America|North\s+America)\s*$',
    re.IGNORECASE,
)

_GEO_THRESHOLD = 5  # min consecutive external-link items to trigger removal


def _find_geo_block_lines(lines: list[str]) -> set[int]:
    """Return indices of lines that belong to geo/language-selector blocks.

    Scans for runs of >= _GEO_THRESHOLD external-link list items, allowing
    blank lines and region sub-headers inside the run. Also absorbs any
    region header + blank lines immediately preceding the run.
    """
    skip: set[int] = set()
    n = len(lines)
    i = 0

    while i < n:
        if not _EXT_LINK_ITEM.match(lines[i]):
            i += 1
            continue

        # Start of a potential run
        run_start = i
        j = i
        link_count = 0
        run_end = i

        while j < n:
            line = lines[j]
            if _EXT_LINK_ITEM.match(line):
                link_count += 1
                run_end = j
                j += 1
            elif line.strip() == "" or _REGION_HEADER.match(line):
                j += 1  # blanks and region sub-headers are allowed inside
            else:
                break

        if link_count >= _GEO_THRESHOLD:
            for k in range(run_start, run_end + 1):
                skip.add(k)
            # Absorb blank lines + one region header directly before the run
            k = run_start - 1
            while k >= 0 and lines[k].strip() == "":
                skip.add(k)
                k -= 1
            if k >= 0 and _REGION_HEADER.match(lines[k]):
                skip.add(k)

        i = run_end + 1

    return skip


# ── helpers ───────────────────────────────────────────────────────────────────

def _parse_frontmatter(text: str) -> tuple[dict, str]:
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


def _header_level(line: str) -> int | None:
    m = _HEADER.match(line)
    return len(m.group(1)) if m else None


def _header_text_normalized(line: str) -> str:
    """Extract header text, strip permalink anchors and markdown formatting."""
    m = _HEADER.match(line)
    if not m:
        return ""
    text = m.group(2)
    text = re.sub(r'\s*\[¶\]\(#[^)]*\)', '', text)  # strip inline permalink
    text = re.sub(r'[*_`\[\]]', '', text)            # strip markdown markers
    return text.strip().lower()


# ── main cleaning logic ───────────────────────────────────────────────────────

def _clean_body(text: str) -> str:
    lines = text.splitlines()
    result: list[str] = []
    i = 0
    skip_until_level: int | None = None

    # ── rule 7 pre-scan: identify geo-block line indices before the main loop
    geo_skip: set[int] = _find_geo_block_lines(lines)

    while i < len(lines):
        line = lines[i]

        # ── rule 7: geo/language-selector block
        if i in geo_skip:
            i += 1
            continue

        # ── rule 4 (inside skip): advance until next header at same/higher level
        if skip_until_level is not None:
            level = _header_level(line)
            if level is not None and level <= skip_until_level:
                skip_until_level = None
                # fall through — process this new header normally
            else:
                i += 1
                continue

        # ── rule 4: navigational header → skip section
        level = _header_level(line)
        if level is not None:
            if _header_text_normalized(line) in _NAV_HEADERS:
                skip_until_level = level
                i += 1
                continue

        # ── rule 2: "On this page" as plain/bold text followed by anchor list
        if _ON_THIS_PAGE_LINE.match(line):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and _ANCHOR_LIST_ITEM.match(lines[j]):
                while j < len(lines) and (
                    _ANCHOR_LIST_ITEM.match(lines[j]) or lines[j].strip() == ""
                ):
                    j += 1
                i = j
                continue

        # ── rule 1: image-only lines
        if _IMAGE_LINE.match(line):
            i += 1
            continue

        # ── rule 3: permalink-only lines
        if _PERMALINK_LINE.match(line):
            i += 1
            continue

        # ── rule 6: bare link lines with fewer than 5 visible words
        m = _BARE_LINK_LINE.match(line)
        if m and len(m.group(1).split()) < 5:
            i += 1
            continue

        result.append(line)
        i += 1

    # ── rule 5: collapse 3+ consecutive blank lines into one
    cleaned = "\n".join(result)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    md_files = sorted(p for p in RAW_DIR.glob("*.md") if p.name != "_errors.log")

    if not md_files:
        print(f"No .md files found in {RAW_DIR}. Run 01_extract.py first.")
        sys.exit(1)

    total_before = 0
    total_after = 0

    for md_path in md_files:
        raw = md_path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(raw)

        before = len(body)
        clean_body = _clean_body(body)
        after = len(clean_body)
        pct = (before - after) / before * 100 if before else 0.0

        total_before += before
        total_after += after

        fm_lines = "\n".join(f"{k}: {v}" for k, v in meta.items())
        output = f"---\n{fm_lines}\n---\n\n{clean_body}"
        (CLEAN_DIR / md_path.name).write_text(output, encoding="utf-8")

        print(f"{md_path.name}: {before:,} -> {after:,} chars  ({pct:.1f}% removido)")

    print("\n" + "=" * 60)
    total_pct = (total_before - total_after) / total_before * 100 if total_before else 0.0
    print(f"Total antes  : {total_before:,} chars")
    print(f"Total depois : {total_after:,} chars")
    print(f"Removido     : {total_before - total_after:,} chars  ({total_pct:.1f}%)")
    print(f"Salvo em     : {CLEAN_DIR}")


if __name__ == "__main__":
    main()
