# Poke Tracker Backend

This backend is a FastAPI app. For local development:

1. Create a virtualenv with Python 3.11.14 (recommended).

2. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn app.main:app --reload --port 8000
```

If you don't have TCGPlayer/EBay API keys the backend will use mocked pricing data. See `.env.example` for env vars.

