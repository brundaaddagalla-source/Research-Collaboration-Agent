from algorithms.external_matching import rank_candidates
from services.llm_service import LLMService


class ExternalResearcherAgent:
    """
    Agent responsible for identifying and ranking
    potential external research collaborators.
    """

    def __init__(self):
        self.name = "External Researcher Agent"
        self.llm_service = LLMService()

    def find_matches(self, researcher, candidates):
        """
        Find and rank external researchers.
        """

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

    def run(self, researcher, candidates):
        """
        Complete external researcher matching workflow.
        """

        ranked_candidates = self.find_matches(
            researcher,
            candidates
        )

        explanation = self.explain_matches(
            researcher,
            ranked_candidates
        )

        return {
            "matches": ranked_candidates,
            "explanation": explanation
        }