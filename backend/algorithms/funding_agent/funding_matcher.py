class FundingMatcher:

    def __init__(self, funding_opportunities):
        self.funding_opportunities = funding_opportunities

    def calculate_score(self, project, funding):

        score = 0

        # --------------------------------
        # 1. Research field match
        # --------------------------------
        project_area = project["research_area"].lower()

        funding_fields = [
            field.lower()
            for field in funding["fields"]
        ]

        if any(field in project_area for field in funding_fields):
            score += 30

        # --------------------------------
        # 2. Keyword match
        # --------------------------------
        project_text = (
            project["project_title"]
            + " "
            + project["project_description"]
        ).lower()

        matched_keywords = 0

        for keyword in funding["keywords"]:
            if keyword.lower() in project_text:
                matched_keywords += 1

        score += min(matched_keywords * 5, 25)

        # --------------------------------
        # 3. Researcher eligibility
        # --------------------------------
        if project["researcher_type"] in funding["eligibility"]:
            score += 20

        # --------------------------------
        # 4. Research stage
        # --------------------------------
        if project["research_stage"] in funding["research_stage"]:
            score += 15

        # --------------------------------
        # 5. Funding amount
        # --------------------------------
        if project["required_amount"] <= funding["amount"]:
            score += 10

        return score

    def find_matches(self, project):

        results = []

        for funding in self.funding_opportunities:

            score = self.calculate_score(
                project,
                funding
            )

            results.append({
                "funding": funding,
                "score": score
            })

        # Highest score first
        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results