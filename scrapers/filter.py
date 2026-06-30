_AI_SIGNALS = [
    "inteligência artificial",
    "machine learning",
    "llm",
    "gpt",
    "modelo de linguagem",
    "nlp",
    "visão computacional",
    "deep learning",
    "ia",
    "automação inteligente",
]


def has_ai_signal(snippet: str) -> bool:
    """Return True if snippet contains at least one AI-related keyword (case-insensitive)."""
    text = snippet.lower()
    return any(signal in text for signal in _AI_SIGNALS)
