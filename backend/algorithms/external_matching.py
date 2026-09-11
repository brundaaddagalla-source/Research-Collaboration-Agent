from typing import List, Dict


def calculate_match_score(
    researcher: Dict,
    candidate: Dict
) -> float:
    """
    Calculate a simple research-match score.

    The score is based on:
    - Research interests
    - Skills
    - Research domain
    """

    score = 0.0

    # Convert values to lowercase sets
    researcher_interests = set(
        interest.lower()
        for interest in researcher.get("research_interests", [])
    )

    candidate_interests = set(
        interest.lower()
        for interest in candidate.get("research_interests", [])
    )

    researcher_skills = set(
        skill.lower()
        for skill in researcher.get("skills", [])
    )

    candidate_skills = set(
        skill.lower()
        for skill in candidate.get("skills", [])
    )

    # Research-interest similarity
    if researcher_interests:
        interest_overlap = (
            researcher_interests & candidate_interests
        )

        interest_score = (
            len(interest_overlap)
            / len(researcher_interests)
        )

        score += interest_score * 0.6

    # Skill similarity
    if researcher_skills:
        skill_overlap = researcher_skills & candidate_skills

        skill_score = (
            len(skill_overlap)
            / len(researcher_skills)
        )

        score += skill_score * 0.4

    return round(score, 4)


def rank_candidates(
    researcher: Dict,
    candidates: List[Dict]
) -> List[Dict]:
    """
    Calculate match scores for all candidates
    and return them in descending order.
    """

    results = []

    for candidate in candidates:

        score = calculate_match_score(
            researcher,
            candidate
        )

        results.append({
            "candidate": candidate,
            "match_score": score
        })

    # Highest score first
    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results