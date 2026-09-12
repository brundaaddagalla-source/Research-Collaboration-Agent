from fastapi import APIRouter, Query

from agents.member1.internal_discovery_agent import (
    discover_internal_collaborations,
)

router = APIRouter()


@router.get("/api/opportunities")
def get_opportunities(
    faculty_name: str = Query(...),
    top_k: int = Query(5, ge=1, le=10),
):
    opportunities = discover_internal_collaborations(
        faculty_name,
        top_k=top_k,
    )

    return {
        "opportunities": opportunities
    }