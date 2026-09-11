from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/funding")
def get_funding():
    """Return mock funding & consortium opportunities."""
    return {"funding_opportunities": source_adapter.get_funding_opportunities()}
