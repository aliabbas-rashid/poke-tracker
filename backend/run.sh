#!/bin/bash
path="ENTER_PATH_TO_YOUR_PROJECT_FOLDER_HERE"
path="$path/poke-tracker/backend"
cd $path || { echo "Path Failure"; exit 1; }
source .venv/bin/activate
python -c "import sys; print('Python:', sys.version); print('Executable:', sys.executable)"
python -c "from app.main import app; print('App loaded:', app)"
uvicorn app.main:app --reload --port 8000

