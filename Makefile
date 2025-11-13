.PHONY: setup run dev test clean

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip setuptools wheel && pip install -r requirements.txt

run:
	env PORT=$${PORT:-8000} uvicorn app.main:app --host 0.0.0.0 --port $${PORT:-8000}

dev:
	uvicorn app.main:app --reload

test:
	pytest -q

clean:
	rm -rf app/data/* .pytest_cache __pycache__
