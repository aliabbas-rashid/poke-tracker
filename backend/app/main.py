try:
    from fastapi import FastAPI
    from .api import portfolios, items, health
except Exception:
    from ._fastapi_fallback import FastAPI
    from .api import portfolios, items, health
from . import db

app = FastAPI(title="Poke Tracker Backend")

@app.on_event("startup")
async def on_startup():
    # create DB tables on startup
    db.init_db()

app.include_router(health.router, prefix="/api")
app.include_router(portfolios.router, prefix="/api")
app.include_router(items.router, prefix="/api")
