# 📄 PDF Text Summarization & Q&A Chatbot (FastAPI)

![Tests](https://github.com/ParikshitJadhav3693/Pdf_Text_Summarization_And_Que_Ans_Chatbot/actions/workflows/tests.yml/badge.svg)



A simple web app to **upload a PDF**, get an **auto‑summary**, and **chat** with the document using retrieval over a TF‑IDF index. Runs **fully offline** by default; if you set `OPENAI_API_KEY`, answers and summaries upgrade to LLM quality automatically.

## Quick Start (no prior coding experience)

### Step 1 — Download & unzip
Unzip this folder. Open a terminal **in this folder**.

### Step 2 — Create a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
```
**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
```

> If installation is slow: it’s downloading SciPy/NumPy/Scikit‑learn wheels; please wait. If an error appears, re‑run `pip install -r requirements.txt` after upgrading pip as shown above.

### Step 3 — Run the app
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Then open **http://localhost:8000/** in your browser.

### Step 4 — Demo
1. Click **Upload PDF** and choose any digital (non‑scanned) PDF (e.g., a syllabus).
2. The app will index it and generate a summary.
3. Type a question in **Chat** and press **Send**.
4. The bot answers and shows **Sources** with relevance scores.

### (Optional) Enable LLM answers
Copy `.env.example` → `.env`, add:
```
OPENAI_API_KEY=sk-...
```
Restart the server. Now answers & summaries are higher quality (abstractive).

---

## Project Structure
```
app/
  main.py              # FastAPI app + static UI
  models.py            # Pydantic models
  routers/
    docs.py            # upload, list, summary
    chat.py            # chat endpoint
  services/
    ingest.py          # parse -> chunk -> index -> summarize -> save
    summarizer.py      # frequency-based summary (local)
    retriever.py       # top-k retrieval + extractive stitch
    providers.py       # optional OpenAI provider
  store/
    vector.py          # TF-IDF store with scikit-learn
  utils/
    pdf.py             # robust PDF text extraction
  static/              # simple single-page UI
docs/
  design.md
  rubric-crosswalk.md
tests/                 # pytest unit tests
```

## Run Tests
```bash
pytest -q
```

## Common Issues
- **PDF has no extractable text:** Use a digital PDF (not a scanned image). OCR is not included in this minimal starter.
- **Port already in use (8000):** Run with a different port: `uvicorn app.main:app --port 8010`.
- **ModuleNotFoundError:** Ensure you activated the virtual environment before running.
- **Windows PowerShell execution policy:** Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` (PowerShell as Admin) once, then re‑activate `.venv`.
