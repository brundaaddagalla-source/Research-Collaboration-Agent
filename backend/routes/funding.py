from fastapi import APIRouter
from pydantic import BaseModel
from adapters import source_adapter
from algorithms.funding_agent.funding_agent import FundingAgent


router = APIRouter(prefix="/api/funding")


class FundingRequest(BaseModel):
    researcher_name: str
    research_area: str
    project_title: str
    project_description: str
    required_amount: float
    research_stage: str
    researcher_type: str


@router.get("")
def get_funding():
    """Return available funding opportunities."""
    return {
        "funding_opportunities": source_adapter.get_funding_opportunities()
    }

@router.post("")
def find_funding(request: FundingRequest):
    project = {
        "researcher_name": request.researcher_name,
        "research_area": request.research_area,
        "project_title": request.project_title,
        "project_description": request.project_description,
        "required_amount": request.required_amount,
        "research_stage": request.research_stage,
        "researcher_type": request.researcher_type,
    }

    agent = FundingAgent()
    results = agent.find_funding(project)

    return {
        "funding_opportunities": results
    }