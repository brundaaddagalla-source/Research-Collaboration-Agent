from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/faculty")
def get_faculty():
    """Return the list of faculty members and their basic research profile."""
    return {"faculty": source_adapter.get_faculty()}
