from typing import List
try:
    from fastapi import APIRouter, Depends, HTTPException
except Exception:
    from .._fastapi_fallback import APIRouter, Depends, HTTPException

# Defensive import for sqlmodel symbols
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

router = APIRouter()

@router.post("/portfolios", response_model=models.Portfolio)
def create_portfolio(portfolio: models.Portfolio):
    with Session(db.engine) as session:
        session.add(portfolio)
        session.commit()
        session.refresh(portfolio)
        return portfolio

@router.get("/portfolios", response_model=List[models.Portfolio])
def list_portfolios():
    with Session(db.engine) as session:
        res = session.exec(select(models.Portfolio)).all()
        return res

@router.get("/portfolios/{portfolio_id}", response_model=models.Portfolio)
def get_portfolio(portfolio_id: int):
    with Session(db.engine) as session:
        p = session.get(models.Portfolio, portfolio_id)
        if not p:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        return p

@router.delete("/portfolios/{portfolio_id}")
def delete_portfolio(portfolio_id: int):
    with Session(db.engine) as session:
        p = session.get(models.Portfolio, portfolio_id)
        if not p:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        session.delete(p)
        session.commit()
        return {"ok": True}

@router.get("/portfolios/{portfolio_id}/value")
def portfolio_value(portfolio_id: int):
    # Simple aggregation: sum latest price snapshots for items
    with Session(db.engine) as session:
        p = session.get(models.Portfolio, portfolio_id)
        if not p:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        total_purchase = 0.0
        total_current = 0.0
        for item in p.items:
            total_purchase += item.purchase_price_gbp
            # get latest price snapshot
            snap = session.exec(select(models.PriceSnapshot).where(models.PriceSnapshot.item_id == item.id).order_by(models.PriceSnapshot.fetched_at.desc())).first()
            if snap:
                total_current += snap.price_gbp
            else:
                total_current += item.purchase_price_gbp
        change_pct = None
        if total_purchase > 0:
            change_pct = ((total_current - total_purchase) / total_purchase) * 100.0
        return {"total_purchase_gbp": total_purchase, "total_current_gbp": total_current, "change_pct": change_pct}
