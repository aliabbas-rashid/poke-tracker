# poke-tracker
Pokemon Collection Value Tracker

This project contains a Python FastAPI backend and a React (Vite) frontend.

Quick start (backend):

1. Create venv with Python 3.11.14, activate it, and install backend dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2. Run the backend:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Quick start (frontend):

1. From `frontend/` run:

```bash
npm install
npm run dev
```

The frontend expects the backend at `http://localhost:8000/api` by default. See `frontend/.env.example` to change.
