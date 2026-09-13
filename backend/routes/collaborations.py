from fastapi import APIRouter, Depends
from pydantic import BaseModel

from adapters import source_adapter
from routes.auth import get_current_faculty
from services import search_orchestrator

router = APIRouter()


@router.get("/api/collaborations")
def get_collaborations(current_faculty: dict = Depends(get_current_faculty)):
    """Return existing collaborations plus a mock node/edge network structure."""
    return {
        "collaborations": source_adapter.get_collaborations(),
        "network": source_adapter.get_collaboration_network(),
    }


# ============================================================
# COLLABORATION SEARCH  (spec sections 10-12, 44)
# ============================================================

class CollaborationSearchIn(BaseModel):
    query: str
    top_k: int = 10


@router.post("/api/collaborations/search")
def search_collaborators(
    payload: CollaborationSearchIn,
    current_faculty: dict = Depends(get_current_faculty),
):
    """
    THE unified faculty search. One free-text research topic fans out,
    behind this single endpoint, to every existing matching engine -
    internal faculty matching, external researcher matching, expertise,
    funding, MoU, and collaboration-network reachability - via
    services/search_orchestrator.py. The current faculty (excluded from
    their own results) always comes from the JWT, never from the request
    body (spec section 10).
    """
    current_faculty_id = int(current_faculty["faculty_id"])
    results = search_orchestrator.unified_search(
        current_faculty_id, payload.query, top_k=payload.top_k
    )
    return {"query": payload.query, "results": results}