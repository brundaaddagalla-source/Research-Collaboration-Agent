from .funding_matcher import FundingMatcher
from .funding_data import FUNDING_OPPORTUNITIES

from services.llm_service import LLMService


class FundingAgent:

    def __init__(self):
        # Initialize funding matcher with funding dataset
        self.matcher = FundingMatcher(FUNDING_OPPORTUNITIES)

        # Initialize LLM service
        self.llm = LLMService()

    def find_funding(self, project):

        # 1. Match project against funding opportunities
        matches = self.matcher.find_matches(project)

        # 2. Keep top 5 opportunities
        top_matches = matches[:5]

        # 3. Generate an explanation for each match
        for result in top_matches:

            funding = result["funding"]
            score = result["score"]

            prompt = f"""
You are a research funding assistant.

Analyze the following research project and funding opportunity.

RESEARCH PROJECT:
Research area: {project["research_area"]}
Project title: {project["project_title"]}
Project description: {project["project_description"]}
Researcher type: {project["researcher_type"]}
Research stage: {project["research_stage"]}
Required amount: {project["required_amount"]}

FUNDING OPPORTUNITY:
Name: {funding.get("name", "Unknown")}
Amount: {funding.get("amount", "Unknown")}
Fields: {funding.get("fields", [])}
Eligibility: {funding.get("eligibility", [])}
Research stages: {funding.get("research_stage", [])}
Keywords: {funding.get("keywords", [])}

MATCH SCORE:
{score}/100

Explain briefly why this funding opportunity is relevant to the project.
Mention the strongest matching factors and any important eligibility or funding considerations.

Do not invent information that is not provided above.
"""

            try:
                explanation = self.llm.generate(prompt)

            except Exception as e:
                explanation = (
                    f"LLM explanation unavailable: {str(e)}"
                )

            result["explanation"] = explanation

        # 4. Return top matches
        return top_matches