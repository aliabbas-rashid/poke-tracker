# Minimal fallbacks for FastAPI symbols so static analysis passes when packages aren't installed
from typing import Callable

class HTTPException(Exception):
    def __init__(self, status_code: int = 500, detail: str = ""):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class APIRouter:
    def __init__(self):
        self.routes = []
    def _decorator(self, *args, **kwargs):
        def inner(fn: Callable):
            return fn
        return inner
    def get(self, *args, **kwargs):
        return self._decorator()
    def post(self, *args, **kwargs):
        return self._decorator()
    def delete(self, *args, **kwargs):
        return self._decorator()

class FastAPI:
    def __init__(self, *args, **kwargs):
        self._routers = []
    def include_router(self, router, prefix: str = ""):
        self._routers.append((prefix, router))
    def on_event(self, name: str):
        def decorator(fn):
            return fn
        return decorator

def Depends(x=None):
    return x

