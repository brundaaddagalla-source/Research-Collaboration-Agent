from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/external-researchers")
def get_external_researchers():
    """Return mock external researcher candidates."""
    return {"external_researchers": source_adapter.get_external_researchers()}
