from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/opportunities")
def get_opportunities():
    """Return mock internal collaboration recommendations."""
    return {"opportunities": source_adapter.get_opportunities()}
