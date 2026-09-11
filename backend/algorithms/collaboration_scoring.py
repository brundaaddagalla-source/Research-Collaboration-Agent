"""
Agent 24 - Collaboration Scoring

Calculates the final strength of a collaboration
opportunity using deterministic scoring.
"""


# --------------------------------------------------
# Scoring weights
# --------------------------------------------------

COMPLEMENTARITY_WEIGHT = 0.30
RESEARCH_RELEVANCE_WEIGHT = 0.25
EVIDENCE_WEIGHT = 0.15
NETWORK_WEIGHT = 0.15
FUNDING_WEIGHT = 0.10
MOU_WEIGHT = 0.05


def clamp_score(score):
    """
    Keep a score between 0 and 1.
    """

    if score is None:
        return 0.0

    return max(
        0.0,
        min(1.0, float(score)),
    )


def calculate_collaboration_score(
    complementarity_score,
    research_relevance_score,
    evidence_score,
    network_score,
    funding_score,
    mou_score,
):
    """
    Calculate the final collaboration score.

    Weights:

    Complementarity       30%
    Research relevance    25%
    Evidence relevance    15%
    Network reachability  15%
    Funding compatibility 10%
    MoU relationship       5%
    """

    complementarity_score = clamp_score(
        complementarity_score
    )

    research_relevance_score = clamp_score(
        research_relevance_score
    )

    evidence_score = clamp_score(
        evidence_score
    )

    network_score = clamp_score(
        network_score
    )

    funding_score = clamp_score(
        funding_score
    )

    mou_score = clamp_score(
        mou_score
    )

    final_score = (
        complementarity_score
        * COMPLEMENTARITY_WEIGHT

        + research_relevance_score
        * RESEARCH_RELEVANCE_WEIGHT

        + evidence_score
        * EVIDENCE_WEIGHT

        + network_score
        * NETWORK_WEIGHT

        + funding_score
        * FUNDING_WEIGHT

        + mou_score
        * MOU_WEIGHT
    )

    return round(
        final_score,
        4,
    )


def get_score_breakdown(
    complementarity_score,
    research_relevance_score,
    evidence_score,
    network_score,
    funding_score,
    mou_score,
):
    """
    Return a transparent breakdown of the
    collaboration score.
    """

    complementarity_score = clamp_score(
        complementarity_score
    )

    research_relevance_score = clamp_score(
        research_relevance_score
    )

    evidence_score = clamp_score(
        evidence_score
    )

    network_score = clamp_score(
        network_score
    )

    funding_score = clamp_score(
        funding_score
    )

    mou_score = clamp_score(
        mou_score
    )

    weighted_scores = {
        "complementarity": round(
            complementarity_score
            * COMPLEMENTARITY_WEIGHT,
            4,
        ),

        "research_relevance": round(
            research_relevance_score
            * RESEARCH_RELEVANCE_WEIGHT,
            4,
        ),

        "evidence": round(
            evidence_score
            * EVIDENCE_WEIGHT,
            4,
        ),

        "network": round(
            network_score
            * NETWORK_WEIGHT,
            4,
        ),

        "funding": round(
            funding_score
            * FUNDING_WEIGHT,
            4,
        ),

        "mou": round(
            mou_score
            * MOU_WEIGHT,
            4,
        ),
    }

    return weighted_scores


def get_opportunity_level(score):
    """
    Convert the final numerical score into
    an easy-to-understand opportunity level.
    """

    score = clamp_score(score)

    if score >= 0.80:
        return "High"

    if score >= 0.65:
        return "Strong"

    if score >= 0.50:
        return "Moderate"

    return "Low"


def score_collaboration(
    complementarity_score,
    research_relevance_score,
    evidence_score,
    network_score,
    funding_score,
    mou_score,
):
    """
    Calculate the complete collaboration scoring result.

    Returns:
        final score
        opportunity level
        individual component scores
        weighted contributions
    """

    final_score = calculate_collaboration_score(
        complementarity_score=
            complementarity_score,

        research_relevance_score=
            research_relevance_score,

        evidence_score=
            evidence_score,

        network_score=
            network_score,

        funding_score=
            funding_score,

        mou_score=
            mou_score,
    )

    breakdown = get_score_breakdown(
        complementarity_score=
            complementarity_score,

        research_relevance_score=
            research_relevance_score,

        evidence_score=
            evidence_score,

        network_score=
            network_score,

        funding_score=
            funding_score,

        mou_score=
            mou_score,
    )

    return {
        "final_score": final_score,

        "opportunity_level":
            get_opportunity_level(
                final_score
            ),

        "component_scores": {
            "complementarity":
                round(
                    clamp_score(
                        complementarity_score
                    ),
                    4,
                ),

            "research_relevance":
                round(
                    clamp_score(
                        research_relevance_score
                    ),
                    4,
                ),

            "evidence":
                round(
                    clamp_score(
                        evidence_score
                    ),
                    4,
                ),

            "network":
                round(
                    clamp_score(
                        network_score
                    ),
                    4,
                ),

            "funding":
                round(
                    clamp_score(
                        funding_score
                    ),
                    4,
                ),

            "mou":
                round(
                    clamp_score(
                        mou_score
                    ),
                    4,
                ),
        },

        "weighted_contributions":
            breakdown,
    }