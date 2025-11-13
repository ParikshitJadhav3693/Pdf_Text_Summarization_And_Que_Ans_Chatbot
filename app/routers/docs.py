\
from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import os, json

from ..services.ingest import ingest_pdf
from ..models import UploadResponse, SummaryResponse, DocumentMeta

DATA_DIR = os.getenv("DATA_DIR", "app/data")

router = APIRouter(prefix="/api", tags=["docs"])

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Please upload a .pdf file")
        data = await file.read()
        doc_id = ingest_pdf(data, file.filename, DATA_DIR)
        return UploadResponse(doc_id=doc_id, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/docs/{doc_id}/summary", response_model=SummaryResponse)
async def get_summary(doc_id: str):
    ddir = Path(DATA_DIR) / doc_id
    if not ddir.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        with open(ddir / "summary.txt", "r", encoding="utf-8") as f:
            summary = f.read().strip()
        with open(ddir / "meta.json", "r", encoding="utf-8") as f:
            meta = DocumentMeta.model_validate_json(f.read())
        return SummaryResponse(summary=summary, meta=meta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/docs")
async def list_docs():
    ddir = Path(DATA_DIR)
    if not ddir.exists():
        return []
    results = []
    for child in ddir.iterdir():
        if not child.is_dir():
            continue
        meta_file = child / "meta.json"
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.loads(f.read())
                results.append(meta)
            except Exception:
                pass
    return results
