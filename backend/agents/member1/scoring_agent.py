"""
Agent 24 - Collaboration Scoring Agent

Orchestrates collaboration scoring without
containing the scoring mathematics itself.
"""

from algorithms.collaboration_scoring import (
    score_collaboration,
)


def score_opportunity(opportunity):
    """
    Score one collaboration opportunity.

    The opportunity is expected to contain
    the component scores produced by the
    collaboration matching pipeline.
    """

    result = score_collaboration(
        complementarity_score=
            opportunity.get(
                "complementarity_score",
                0.0,
            ),

        research_relevance_score=
            opportunity.get(
                "semantic_similarity",
                0.0,
            ),

        evidence_score=
            opportunity.get(
                "evidence_relevance",
                0.0,
            ),

        network_score=
            opportunity.get(
                "network_score",
                0.0,
            ),

        funding_score=
            opportunity.get(
                "funding_score",
                0.0,
            ),

        mou_score=
            opportunity.get(
                "mou_score",
                0.0,
            ),
    )

    scored_opportunity = dict(
        opportunity
    )

    scored_opportunity[
        "collaboration_score"
    ] = result[
        "final_score"
    ]

    scored_opportunity[
        "opportunity_level"
    ] = result[
        "opportunity_level"
    ]

    scored_opportunity[
        "score_breakdown"
    ] = result[
        "component_scores"
    ]

    scored_opportunity[
        "weighted_contributions"
    ] = result[
        "weighted_contributions"
    ]

    return scored_opportunity


def score_opportunities(opportunities):
    """
    Score multiple collaboration opportunities.
    """

    scored_opportunities = []

    for opportunity in opportunities:

        scored = score_opportunity(
            opportunity
        )

        scored_opportunities.append(
            scored
        )

    scored_opportunities.sort(
        key=lambda item:
            item.get(
                "collaboration_score",
                0.0,
            ),
        reverse=True,
    )

    return scored_opportunities