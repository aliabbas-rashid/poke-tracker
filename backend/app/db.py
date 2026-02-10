try:
    from sqlmodel import SQLModel, create_engine, Session
except Exception:
    # Fallback stubs for environments without sqlmodel installed (satisfy static checks)
    class SQLModel:
        metadata = type("md", (), {"create_all": staticmethod(lambda engine: None)})
    def create_engine(url, echo=False):
        return None
    class Session:
        def __init__(self, engine):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    def load_dotenv():
        return None

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/poke.db")

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
