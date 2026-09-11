from fastapi import APIRouter
from adapters import source_adapter

router = APIRouter()


@router.get("/api/collaborations")
def get_collaborations():
    """Return existing collaborations plus a mock node/edge network structure."""
    return {
        "collaborations": source_adapter.get_collaborations(),
        "network": source_adapter.get_collaboration_network(),
    }
