try:
    from fastapi import APIRouter
except Exception:
    from .._fastapi_fallback import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}
