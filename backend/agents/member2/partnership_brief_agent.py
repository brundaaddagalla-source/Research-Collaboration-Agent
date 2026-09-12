from services.llm_service import LLMService


class PartnershipBriefAgent:
    """
    Agent responsible for generating
    research partnership / introduction briefs.
    """

    def __init__(self):
        self.name = "Partnership Brief Agent"
        self.llm_service = LLMService()

    def generate_brief(
        self,
        faculty,
        external_researcher,
        funding=None,
        mou=None
    ):
        """
        Generate a partnership brief using
        the available research information.
        """

        prompt = f"""
You are a research collaboration assistant.

Create a concise partnership brief between
an internal university researcher and an external researcher.

INTERNAL RESEARCHER

Name:
{faculty.get("name", "Unknown")}

Department:
{faculty.get("department", "Unknown")}

Research Areas:
{faculty.get("research_areas", [])}

PUBLICATIONS:
{faculty.get("publications", [])}

PROJECTS:
{faculty.get("projects", [])}


EXTERNAL RESEARCHER

Name:
{external_researcher.get("name", "Unknown")}

Institution:
{external_researcher.get("institution", "Unknown")}

Country:
{external_researcher.get("country", "Unknown")}

Research Interests:
{external_researcher.get("research_interests", [])}

Skills:
{external_researcher.get("skills", [])}

Research Area:
{external_researcher.get("research_area", "Unknown")}

Research Fit:
{external_researcher.get("research_fit", "Unknown")}

Network Reachability:
{external_researcher.get("network_reachability", "Unknown")}


FUNDING OPPORTUNITY

{funding if funding else "No funding opportunity provided."}


MoU INFORMATION

{mou if mou else "No existing MoU information provided."}


Generate the response using these sections:

1. Partnership Opportunity
2. Complementary Expertise
3. Potential Collaboration Topic
4. Relevant Funding
5. Existing MoU Relationship
6. Recommended Next Step

Keep the brief concise and useful for a university
research office.

Do not invent facts.

If information is unavailable, explicitly say
that it is not available.
"""

        return self.llm_service.generate(prompt)

    def run(
        self,
        faculty,
        external_researcher,
        funding=None,
        mou=None
    ):
        """
        Generate the final partnership brief.
        """

        brief = self.generate_brief(
            faculty,
            external_researcher,
            funding,
            mou
        )

        return {
            "faculty": faculty,
            "external_researcher": external_researcher,
            "funding": funding,
            "mou": mou,
            "brief": brief,
        }