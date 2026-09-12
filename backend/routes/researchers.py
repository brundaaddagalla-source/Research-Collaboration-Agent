from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.member2.external_researcher_agent import ExternalResearcherAgent

router = APIRouter()


class ResearcherProfile(BaseModel):
    name: str
    research_interests: list[str] = []
    skills: list[str] = []


@router.get("/api/external-researchers")
def get_external_researchers():
    """Return external researcher candidates via the External Researcher Agent."""
    agent = ExternalResearcherAgent()
    return {"external_researchers": agent.get_candidates()}


@router.post("/api/external-researchers/match")
def match_external_researchers(profile: ResearcherProfile):
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