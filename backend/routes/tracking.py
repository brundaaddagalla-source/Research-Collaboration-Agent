from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/tracking")
def get_tracking():
    """Return mock collaboration pipeline records and the pipeline stages."""
    return {
        "stages": source_adapter.get_tracking_stages(),
        "records": source_adapter.get_tracking_records(),
    }
