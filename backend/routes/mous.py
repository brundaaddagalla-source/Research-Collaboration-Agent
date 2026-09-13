from fastapi import APIRouter
from agents.member2.mou_agent import MoUAgent

router = APIRouter()


@router.get("/api/mous")
def get_mous():
    """Return MoU records and a status breakdown via the MoU Intelligence Agent."""
    agent = MoUAgent()
    result = agent.run()

    return {
        "mous": result["all_mous"],
        "summary": {
            "total_mous": result["total_mous"],
            "active": len(result["active_mous"]),
            "underutilized": len(result["underutilized_mous"]),
            "dormant": len(result["dormant_mous"]),
        },
    }