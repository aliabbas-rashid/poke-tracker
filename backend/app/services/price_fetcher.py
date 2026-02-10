# Simple price fetcher that returns mocked data or uses adapters when available
from typing import Dict, Any
import os
from .. import db, models
try:
    from sqlmodel import Session, select
except Exception:
    class Session:
        def __init__(self, engine):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False
    def select(x):
        return None
from datetime import datetime
try:
    from cachetools import TTLCache, cached
except Exception:
    # lightweight fallback cache
    class TTLCache(dict):
        def __init__(self, maxsize=1000, ttl=300):
            super().__init__()
    def cached(cache):
        def decorator(fn):
            return fn
        return decorator

CACHE_TTL = int(os.getenv("API_CACHE_TTL_SECONDS", "300"))
cache = TTLCache(maxsize=1000, ttl=CACHE_TTL)

def _mock_price_for_item(item: models.Item) -> Dict[str, Any]:
    # Returns a mocked price slightly above purchase price
    try:
        base = float(item.purchase_price_gbp or 0.0)
    except Exception:
        base = 0.0
    return {"price_gbp": round(base * 1.1, 2), "currency": "GBP", "source": "mock"}

@cached(cache)
def get_current_price_for_item(item_id: int) -> Dict[str, Any]:
    try:
        with Session(db.engine) as session:
            item = session.get(models.Item, item_id) if hasattr(session, 'get') else None
    except Exception:
        item = None
    if not item:
        # Try to construct a minimal item stub from DB using SQLModel if available
        return {"error": "Item not found"}
    # Try adapters (not implemented) - fall back to mock
    res = _mock_price_for_item(item)
    return {"item_id": item_id, "price_gbp": res["price_gbp"], "currency": res["currency"], "source": res["source"], "fetched_at": datetime.utcnow().isoformat()}


def fetch_and_store_price_for_item(item_id: int) -> Dict[str, Any]:
    price = get_current_price_for_item(item_id)
    # store into PriceSnapshot
    try:
        with Session(db.engine) as session:
            snap = models.PriceSnapshot(item_id=item_id, price_gbp=price.get("price_gbp", 0.0), source=price.get("source"))
            session.add(snap)
            session.commit()
            session.refresh(snap)
            return {"ok": True, "snapshot_id": getattr(snap, 'id', None), "price": price}
    except Exception:
        return {"ok": False, "error": "unable to store snapshot in current environment"}
