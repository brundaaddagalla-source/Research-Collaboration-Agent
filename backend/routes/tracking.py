from fastapi import APIRouter
from adapters import source_adapter
from agents.member2.tracking_agent import TrackingAgent

router = APIRouter()


@router.get("/api/tracking")
def get_tracking():
    """Return the collaboration pipeline stages and records via the Tracking Agent."""
    agent = TrackingAgent()

    return {
        "stages": source_adapter.get_tracking_stages(),
        "records": agent.get_tracking_records(),
        "stage_summary": agent.get_stage_summary(),
    }
