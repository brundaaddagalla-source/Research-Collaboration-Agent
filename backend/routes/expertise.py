from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/expertise")
def get_expertise():
    """Return mock research-area -> faculty-count mapping (the future Expertise Map)."""
    return {"expertise_map": source_adapter.get_expertise_map()}
