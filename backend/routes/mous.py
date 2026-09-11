from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/mous")
def get_mous():
    """Return mock MoU records with mock status classification."""
    return {"mous": source_adapter.get_mous()}
