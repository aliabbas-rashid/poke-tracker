#!/bin/bash
cd /Users/aliabbasrashid/PycharmProjects/poke-tracker/backend
source .venv/bin/activate
python -c "import sys; print('Python:', sys.version); print('Executable:', sys.executable)"
python -c "from app.main import app; print('App loaded:', app)"
uvicorn app.main:app --reload --port 8000

