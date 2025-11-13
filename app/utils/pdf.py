\
from __future__ import annotations
from io import BytesIO
import re

def normalize_text(text: str) -> str:
    text = text.replace("\x0c", " ").replace("\r", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def extract_text_from_pdf_bytes(data: bytes) -> str:
    """
    Try pypdf first; if empty, fall back to pdfminer.six
    """
    # pypdf
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(BytesIO(data))
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        text = "\n".join(pages)
        if text and len(text.strip()) > 0:
            return normalize_text(text)
    except Exception:
        pass

    # pdfminer fallback
    try:
        from pdfminer.high_level import extract_text  # type: ignore
        with BytesIO(data) as bio:
            text = extract_text(bio) or ""
        return normalize_text(text)
    except Exception as e:
        raise RuntimeError(f"Could not extract text from PDF: {e}")
