from __future__ import annotations
from fastapi import APIRouter, HTTPException
import os
from pathlib import Path

from ..models import ChatRequest, ChatResponse, SourceChunk
from ..services.retriever import retrieve_topk, stitch_answer, rule_based_answer
from ..services.providers import openai_answer

DATA_DIR = os.getenv("DATA_DIR", "app/data")
router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    ddir = Path(DATA_DIR) / req.doc_id
    if not ddir.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        # Retrieve a few more chunks for better recall
        triples = retrieve_topk(ddir, req.message, k=8)
        sources = [SourceChunk(idx=i, score=s, chunk=c) for (i, s, c) in triples]
        contexts = [c for (_, _, c) in triples]

        # 1) Rule-based answers (fast & precise; handles lease facts, author/source/date,
        #    photosynthesis pack, etc.)
        answer = rule_based_answer(req.message, contexts)

        # 2) LLM (optional; returns None if no OPENAI_API_KEY or on failure)
        if answer is None:
            answer = openai_answer(req.message, contexts)

        # 3) Offline extractive fallback (always available)
        if answer is None:
            answer = stitch_answer(req.message, contexts, max_sentences=5)

        return ChatResponse(answer=answer, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
