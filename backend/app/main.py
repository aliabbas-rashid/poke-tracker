try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from .api import portfolios, items, health
except Exception:
    from ._fastapi_fallback import FastAPI
    try:
        from fastapi.middleware.cors import CORSMiddleware
    except Exception:
        class CORSMiddleware:
            def __init__(self, *args, **kwargs):
                pass
    from .api import portfolios, items, health
from . import db

app = FastAPI(title="Poke Tracker Backend")

# Add CORS middleware to allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Poke Tracker API", "docs": "http://localhost:8000/docs"}

@app.on_event("startup")
async def on_startup():
    # create DB tables on startup
    db.init_db()

app.include_router(health.router, prefix="/api")
app.include_router(portfolios.router, prefix="/api")
app.include_router(items.router, prefix="/api")
