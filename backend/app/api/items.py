# Defensive imports like portfolios module
try:
    from fastapi import APIRouter, HTTPException
except Exception:
    from .._fastapi_fallback import APIRouter, HTTPException
try:
    from sqlmodel import select, Session
except Exception:
    def select(x=None):
        class Q:
            def where(self, *args, **kwargs):
                return self
            def order_by(self, *args, **kwargs):
                return self
            def asc(self):
                return self
            def desc(self):
                return self
        return Q()
    class Session:
        def __init__(self, engine):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False
        def exec(self, q):
            class R:
                def all(self):
                    return []
                def first(self):
                    return None
            return R()
        def get(self, model, id):
            return None

from .. import db, models
from typing import List

router = APIRouter()

@router.post("/portfolios/{portfolio_id}/items", response_model=models.Item)
def create_item(portfolio_id: int, item: models.Item):
    with Session(db.engine) as session:
        portfolio = session.get(models.Portfolio, portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        item.portfolio_id = portfolio_id
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@router.get("/items/{item_id}", response_model=models.Item)
def get_item(item_id: int):
    with Session(db.engine) as session:
        it = session.get(models.Item, item_id)
        if not it:
            raise HTTPException(status_code=404, detail="Item not found")
        return it

@router.get("/items/{item_id}/price")
def get_item_price(item_id: int):
    from ..services.price_fetcher import get_current_price_for_item
    with Session(db.engine) as session:
        it = session.get(models.Item, item_id)
        if not it:
            raise HTTPException(status_code=404, detail="Item not found")
    price = get_current_price_for_item(item_id)
    return price

@router.get("/items/{item_id}/history")
def get_item_history(item_id: int):
    with Session(db.engine) as session:
        snaps = session.exec(select(models.PriceSnapshot).where(models.PriceSnapshot.item_id == item_id).order_by(models.PriceSnapshot.fetched_at.asc())).all()
        return snaps

# simple endpoint to fetch and store latest price
@router.post("/items/{item_id}/refresh_price")
def refresh_price(item_id: int):
    from ..services.price_fetcher import fetch_and_store_price_for_item
    res = fetch_and_store_price_for_item(item_id)
    return res
