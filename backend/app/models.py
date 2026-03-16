from typing import Optional
try:
    from sqlmodel import SQLModel, Field, Relationship
except Exception:
    class SQLModel:
        @classmethod
        def __init_subclass__(cls, *args, **kwargs):
            # accept arbitrary kwargs like table=True in subclass definitions
            return None
    def Field(*args, **kwargs):
        return None
    def Relationship(*args, **kwargs):
        return None

from datetime import datetime
from typing import List

class Portfolio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    items: List["Item"] = Relationship(back_populates="portfolio")

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    portfolio_id: int = Field(foreign_key="portfolio.id")
    name: str
    category: Optional[str] = None  # sealed/raw/graded
    purchase_price_gbp: float = 0.0
    purchase_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    portfolio: Optional[Portfolio] = Relationship(back_populates="items")

class PriceSnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    price_gbp: float
    source: Optional[str] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
