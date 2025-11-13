from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class DocumentMeta(BaseModel):
    id: str
    filename: str
    created_at: datetime
    chunk_size: int
    overlap: int
    num_chunks: int

class UploadResponse(BaseModel):
    doc_id: str
    filename: str

class SummaryResponse(BaseModel):
    summary: str
    meta: DocumentMeta

class SourceChunk(BaseModel):
    idx: int
    score: float
    chunk: str

class ChatRequest(BaseModel):
    doc_id: str
    message: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
