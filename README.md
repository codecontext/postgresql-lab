# PostgreSQL Learning Lab

A small, hands-on environment for learning PostgreSQL. The application is
currently a minimal FastAPI foundation; database connections and learning
features will be added incrementally.

## Requirements

- Python 3.10 or later
- PostgreSQL, when database connectivity is introduced

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/health> to check that the API is running.