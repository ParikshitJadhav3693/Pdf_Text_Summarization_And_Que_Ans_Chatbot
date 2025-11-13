\
from __future__ import annotations
import os
from typing import List, Optional

def _openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None

def openai_summarize(chunks: List[str], max_tokens: int = 300) -> Optional[str]:
    client = _openai_client()
    if client is None:
        return None
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = (
        "Summarize the document faithfully in 4-6 bullet points. Use only the provided text.\\n\\n"
        + "\\n\\n".join(chunks)[:12000]
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You summarize and answer questions strictly from given text."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None

def openai_answer(question: str, contexts: List[str], max_tokens: int = 350) -> Optional[str]:
    client = _openai_client()
    if client is None:
        return None
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    context_str = "\\n\\n".join([f"[Chunk {i+1}]\\n{c}" for i, c in enumerate(contexts)])
    prompt = (
        "Answer the question using ONLY the provided chunks. "
        "If the answer is not present, say you cannot find it in the document.\\n\\n"
        f"{context_str}\\n\\nQuestion: {question}\\nAnswer:"
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You answer strictly from provided context and are concise."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None
