from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agents.member2.external_researcher_agent import ExternalResearcherAgent
from routes.auth import get_current_faculty

router = APIRouter()


class ResearcherProfile(BaseModel):
    name: str
    research_interests: list[str] = []
    skills: list[str] = []


@router.get("/api/external-researchers")
def get_external_researchers(current_faculty: dict = Depends(get_current_faculty)):
    """Return external researcher candidates via the External Researcher Agent."""
    agent = ExternalResearcherAgent()
    return {"external_researchers": agent.get_candidates()}


@router.post("/api/external-researchers/match")
def match_external_researchers(
    profile: ResearcherProfile, current_faculty: dict = Depends(get_current_faculty)
):
    """
    Rank external researcher candidates against a given profile and
    generate an LLM explanation of the best matches.

    Requires FREELLMAPI_API_KEY to be configured in the backend .env file.
    """
    agent = ExternalResearcherAgent()

    try:
        result = agent.run(profile.model_dump())
    except ValueError as exc:
        # Raised by LLMService.generate() when no API key is configured.
        raise HTTPException(status_code=503, detail=str(exc))

    return result