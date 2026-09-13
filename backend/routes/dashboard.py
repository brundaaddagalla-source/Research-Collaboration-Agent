from fastapi import APIRouter
from adapters import source_adapter
from agents.member2.mou_agent import MoUAgent
from agents.member2.impact_agent import ImpactAgent
from agents.member2.external_researcher_agent import ExternalResearcherAgent

router = APIRouter()


@router.get("/api/dashboard")
def get_dashboard():
    """Return top-level KPI summary + collaboration activity for the dashboard page."""
    mou_result = MoUAgent().run()
    impact = ImpactAgent().calculate_impact()
    external_candidates = ExternalResearcherAgent().get_candidates()

    base_summary = source_adapter.get_dashboard_summary()

    summary = {
        **base_summary,
        "external_candidates": len(external_candidates),
        "dormant_mous": len(mou_result["dormant_mous"]),
        # Real pipeline count from the Tracking/Impact agent instead of a
        # hardcoded 0. The Dashboard page overrides this with a live,
        # faculty-specific count from /api/opportunities, so this value
        # mainly matters for any other consumer of this endpoint.
        "potential_collaborations": impact["total_collaborations"],
    }

    return {
        "summary": summary,
        "collaboration_activity": source_adapter.get_collaboration_activity(),
        "top_opportunities": source_adapter.get_opportunities()[:3],
        "funding_highlights": source_adapter.get_funding_opportunities()[:3],
        "mou_highlights": mou_result["all_mous"],
    }