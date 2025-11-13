\
from __future__ import annotations
from typing import List
import os, json, uuid, re
from datetime import datetime
from pathlib import Path

from ..utils.pdf import extract_text_from_pdf_bytes, normalize_text
from .summarizer import frequency_summarize
from ..store.vector import TfidfVectorStore
from ..models import DocumentMeta

DEFAULT_CHUNK_SIZE = 180
DEFAULT_OVERLAP = 30

_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")

def split_into_sentences(text: str) -> List[str]:
    text = normalize_text(text)
    sents = _SENT_SPLIT_RE.split(text)
    return [s.strip() for s in sents if s and not s.isspace()]

def chunk_sentences(sents: List[str], chunk_size_words: int = DEFAULT_CHUNK_SIZE, overlap_words: int = DEFAULT_OVERLAP) -> List[str]:
    if not sents:
        return []
    chunks: List[str] = []
    curr_words: List[str] = []
    total_words = 0

    def flush():
        if curr_words:
            chunks.append(" ".join(curr_words).strip())

    i = 0
    while i < len(sents):
        sent = sents[i]
        words = sent.split()
        if total_words + len(words) > chunk_size_words and total_words > 0:
            flush()
            if overlap_words > 0:
                overlap = curr_words[-overlap_words:] if len(curr_words) > overlap_words else curr_words
                curr_words = overlap.copy()
                total_words = len(curr_words)
            else:
                curr_words = []
                total_words = 0
        curr_words.extend(words)
        total_words += len(words)
        i += 1
    flush()
    return [c for c in chunks if c]

def save_document(doc_id: str, filename: str, chunks: List[str], store: TfidfVectorStore, summary: str, base_dir: str):
    ddir = Path(base_dir) / doc_id
    ddir.mkdir(parents=True, exist_ok=True)
    with open(ddir / "chunks.json", "w", encoding="utf-8") as f:
        json.dump([{"idx": i, "text": c} for i, c in enumerate(chunks)], f, ensure_ascii=False, indent=2)
    store.save(ddir / "index.pkl")
    with open(ddir / "summary.txt", "w", encoding="utf-8") as f:
        f.write(summary.strip())

    meta = DocumentMeta(
        id=doc_id,
        filename=filename,
        created_at=datetime.utcnow(),
        chunk_size=DEFAULT_CHUNK_SIZE,
        overlap=DEFAULT_OVERLAP,
        num_chunks=len(chunks),
    )
    with open(ddir / "meta.json", "w", encoding="utf-8") as f:
        f.write(meta.model_dump_json(indent=2))

def ingest_pdf(file_bytes: bytes, filename: str, data_dir: str) -> str:
    text = extract_text_from_pdf_bytes(file_bytes)
    if not text or not text.strip():
        raise RuntimeError("The uploaded PDF did not contain extractable text. Please use a digital (non-scanned) PDF.")
    sentences = split_into_sentences(text)
    chunks = chunk_sentences(sentences, DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP)

    store = TfidfVectorStore.fit_from_chunks(chunks)
    summary = frequency_summarize(" ".join(chunks), max_sentences=6)

    doc_id = str(uuid.uuid4())[:8]
    save_document(doc_id, filename, chunks, store, summary, data_dir)
    return doc_id
