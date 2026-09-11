from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/dashboard")
def get_dashboard():
    """Return top-level KPI summary + collaboration activity for the dashboard page."""
    return {
        "summary": source_adapter.get_dashboard_summary(),
        "collaboration_activity": source_adapter.get_collaboration_activity(),
        "top_opportunities": source_adapter.get_opportunities()[:3],
        "funding_highlights": source_adapter.get_funding_opportunities()[:3],
        "mou_highlights": source_adapter.get_mous(),
    }
