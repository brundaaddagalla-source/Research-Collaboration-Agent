from algorithms.external_matching import rank_candidates
from services.llm_service import LLMService

from database.connection import SessionLocal
from models.models import ExternalResearcher


class ExternalResearcherAgent:
    """
    Agent responsible for identifying and ranking
    potential external research collaborators.
    """

    def __init__(self):
        self.name = "External Researcher Agent"
        self.llm_service = LLMService()

    def get_candidates(self):
        """
        Get external researcher candidates from the database.
        """

        db = SessionLocal()

        try:
            researchers = db.query(ExternalResearcher).all()

            candidates = []

            for researcher in researchers:
                candidates.append({
                    "id": researcher.id,
                    "name": researcher.name,
                    "institution": researcher.institution,
                    "country": researcher.country,
                    "research_interests": researcher.research_interests or [],
                    "skills": researcher.skills or [],
                    "research_area": researcher.research_area,
                    "research_fit": researcher.research_fit,
                    "network_reachability": researcher.network_reachability,
                    "overall_score": researcher.overall_score,
                })

            return candidates

        finally:
            db.close()

    def find_matches(self, researcher, candidates=None):
        """
        Find and rank external researchers.

        If candidates are not provided, candidates are
        loaded from the database.
        """

        if candidates is None:
            candidates = self.get_candidates()

        ranked_candidates = rank_candidates(
            researcher,
            candidates
        )

        return ranked_candidates

    def explain_matches(self, researcher, ranked_candidates):
        """
        Use the LLM to generate a human-readable
        explanation of the best research matches.
        """

        prompt = f"""
You are a research collaboration assistant.

A researcher has the following profile:

Name:
{researcher.get("name", "Unknown")}

Research interests:
{researcher.get("research_interests", [])}

Skills:
{researcher.get("skills", [])}

The following researchers were identified as potential matches:

{ranked_candidates}

Explain the top research collaboration opportunities.

For each strong match:

1. Give the researcher's name.
2. Explain why they are a good match.
3. Mention overlapping research interests.
4. Mention relevant skills.
5. Keep the explanation concise.

Do not invent information that is not present in the data.
"""

        return self.llm_service.generate(prompt)

    def run(self, researcher):
        """
        Complete external researcher matching workflow.

        External researcher candidates are loaded from
        the database.
        """

        ranked_candidates = self.find_matches(
            researcher
        )

        explanation = self.explain_matches(
            researcher,
            ranked_candidates
        )

        return {
            "matches": ranked_candidates,
            "explanation": explanation
        }
