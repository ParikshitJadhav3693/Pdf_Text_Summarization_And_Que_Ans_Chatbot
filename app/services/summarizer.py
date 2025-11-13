\
from __future__ import annotations
from typing import List
import re
from collections import Counter

STOP = {
    "the","a","an","of","to","and","or","in","on","for","by","with","is","are","was","were","be","been","being",
    "at","from","as","that","this","it","its","into","but","not","no","can","could","should","would","may","might",
    "will","just","than","then","so","such","if","about","over","under","between","more","most","less","least",
    "also","we","you","they","he","she","them","their","our","us","i"
}

_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")

def _sentences(text: str) -> List[str]:
    sents = _SENT_SPLIT_RE.split(text.strip())
    return [s.strip() for s in sents if s.strip()]

def _normalize(token: str) -> str:
    token = re.sub(r"[^a-z0-9]", "", token.lower())
    return token

def frequency_summarize(text: str, max_sentences: int = 5) -> str:
    sents = _sentences(text)
    if len(sents) <= max_sentences:
        return " ".join(sents)

    freqs = Counter()
    for s in sents:
        for w in s.split():
            w = _normalize(w)
            if not w or w in STOP: continue
            freqs[w] += 1
    if not freqs:
        return " ".join(sents[:max_sentences])

    scored = []
    for i, s in enumerate(sents):
        score = 0.0
        words = s.split()
        for w in words:
            w = _normalize(w)
            if not w or w in STOP: continue
            score += freqs[w]
        score = score / (len(words) + 1e-6)
        scored.append((i, score))

    top = sorted(scored, key=lambda x: x[1], reverse=True)[:max_sentences]
    idxs = sorted([i for i, _ in top])
    return " ".join([sents[i] for i in idxs])
