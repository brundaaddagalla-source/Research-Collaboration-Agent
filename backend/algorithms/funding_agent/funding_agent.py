from .funding_matcher import FundingMatcher
from services.llm_service import LLMService

from database.connection import SessionLocal
from models.models import FundingCall


class FundingAgent:

    def __init__(self):
        # Initialize LLM service
        self.llm = LLMService()

    def get_funding_opportunities(self):
        """
        Get funding opportunities from the database.
        """

        db = SessionLocal()

        try:
            funding_records = db.query(FundingCall).all()

            funding_opportunities = []

            for funding in funding_records:
                funding_opportunities.append({
                    "id": funding.id,
                    "name": funding.name,
                    "organization": funding.organization,
                    "amount": funding.amount,
                    "deadline": (
                        funding.deadline.isoformat()
                        if funding.deadline
                        else None
                    ),
                    "fields": funding.fields or [],
                    "eligibility": funding.eligibility or [],
                    "research_stage": funding.research_stage or [],
                    "keywords": funding.keywords or [],
                    "consortium_requirement": (
                        funding.consortium_requirement
                    ),
                    "international_partner_required": (
                        funding.international_partner_required
                    ),
                    "industry_partner_required": (
                        funding.industry_partner_required
                    ),
                    "matching_faculty": (
                        funding.matching_faculty or []
                    ),
                })

            return funding_opportunities

        finally:
            db.close()

    def find_funding(self, project):

        # 1. Get funding opportunities from database
        funding_opportunities = self.get_funding_opportunities()

        # 2. Initialize funding matcher with database data
        matcher = FundingMatcher(
            funding_opportunities
        )

        # 3. Match project against funding opportunities
        matches = matcher.find_matches(project)

        # 4. Keep top 5 opportunities
        top_matches = matches[:5]

        # 5. Generate an explanation for each match
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

Organization: {funding.get("organization", "Unknown")}

Amount: {funding.get("amount", "Unknown")}

Deadline: {funding.get("deadline", "Unknown")}

Fields: {funding.get("fields", [])}

Eligibility: {funding.get("eligibility", [])}

Research stages: {funding.get("research_stage", [])}

Keywords: {funding.get("keywords", [])}

Consortium required:
{funding.get("consortium_requirement", False)}

International partner required:
{funding.get("international_partner_required", False)}

Industry partner required:
{funding.get("industry_partner_required", False)}

MATCH SCORE:

{score}/100

Explain briefly why this funding opportunity is relevant to the project.

Mention the strongest matching factors and any important
eligibility, deadline, consortium, or funding considerations.

Do not invent information that is not provided above.
"""

            try:
                explanation = self.llm.generate(prompt)

            except Exception as e:
                explanation = (
                    f"LLM explanation unavailable: {str(e)}"
                )

            result["explanation"] = explanation

        # 6. Return top matches
        return top_matches