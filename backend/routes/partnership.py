from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.member2.partnership_brief_agent import PartnershipBriefAgent

router = APIRouter()


class FacultyInput(BaseModel):
    name: str
    department: Optional[str] = None
    research_areas: list = []
    publications: list = []
    projects: list = []


class ExternalResearcherInput(BaseModel):
    name: str
    institution: Optional[str] = None
    country: Optional[str] = None
    research_interests: list = []
    skills: list = []
    research_area: Optional[str] = None
    research_fit: Optional[float] = None
    network_reachability: Optional[str] = None


class PartnershipBriefRequest(BaseModel):
    faculty: FacultyInput
    external_researcher: ExternalResearcherInput
    funding: Optional[dict] = None
    mou: Optional[dict] = None


@router.post("/api/partnership-brief")
def generate_partnership_brief(request: PartnershipBriefRequest):
    """
    Generate an LLM-written partnership brief between an internal
    faculty member and an external researcher.

    Requires FREELLMAPI_API_KEY to be configured in the backend .env file.
    """
    agent = PartnershipBriefAgent()

    try:
        result = agent.run(
            faculty=request.faculty.model_dump(),
            external_researcher=request.external_researcher.model_dump(),
            funding=request.funding,
            mou=request.mou,
        )
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    return result