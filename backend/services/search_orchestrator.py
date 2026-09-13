"""
Unified collaboration search orchestration (product requirement:
"ALL ALGORITHMS WORK BEHIND THE SEARCH").

This module does NOT implement any new matching/scoring logic. It calls
the existing, independently-owned engines and reshapes their output into
one ranked list so the faculty-facing search box is the only place these
capabilities are surfaced:

  services.matching_service
      -> internal faculty candidates
         (score, expertise, publications, projects, research documents,
          funding, MoU - all computed from real DB rows)

  algorithms.collaboration_matching
      -> real collaboration-graph network reachability between the current
         faculty and each internal candidate, and funding/MoU relevance

  agents.member2.external_researcher_agent
      -> external researcher ranking
         (algorithms/external_matching.py)

Nothing here implements a new matching/scoring algorithm. It only
orchestrates the existing engines and merges their responses.
"""

from database.connection import SessionLocal
from models.models import Faculty, Collaboration, FundingCall, MoU
from services import matching_service
from agents.member2.external_researcher_agent import ExternalResearcherAgent

from algorithms.collaboration_matching import (
    build_collaboration_graph,
    network_distance,
    reachability_label,
    calculate_network_score,
    find_relevant_funding,
    find_relevant_mou,
)


def _faculty_id_graph(db):
    """
    Build the real collaboration graph using the existing
    collaboration_matching algorithm and actual Collaboration rows.
    """
    name_to_id = {
        name: faculty_id
        for faculty_id, name in db.query(Faculty.id, Faculty.name).all()
    }

    pairs = []

    for collaboration in db.query(Collaboration).all():
        faculty_a_id = name_to_id.get(collaboration.faculty_a)
        faculty_b_id = name_to_id.get(collaboration.faculty_b)

        if faculty_a_id is not None and faculty_b_id is not None:
            pairs.append(
                {
                    "faculty_a_id": faculty_a_id,
                    "faculty_b_id": faculty_b_id,
                }
            )

    return build_collaboration_graph(pairs)


def _enrich_internal_with_network(
    db,
    current_faculty_id,
    internal_results,
):
    """
    Attach real network reachability and network score to each
    internal candidate.

    The network calculations themselves remain inside
    algorithms.collaboration_matching.
    """
    graph = _faculty_id_graph(db)

    for result in internal_results:
        candidate_id = int(result["faculty"]["faculty_id"])

        distance = network_distance(
            graph,
            current_faculty_id,
            candidate_id,
        )

        result["network_distance"] = distance
        result["network_reachability"] = reachability_label(distance)
        result["network_score"] = calculate_network_score(distance)
        result["result_type"] = "internal"

    return internal_results


def _external_results(db, query, top_k):
    """
    Rank external researchers for the same free-text query using the
    existing ExternalResearcherAgent / external_matching algorithm.

    Funding and MoU relevance are attached using the existing
    collaboration_matching helpers.

    External matching is additive: if it fails, internal faculty search
    still works normally.
    """
    query = query.strip()

    if not query:
        return []

    query_tokens = matching_service.tokenize(query)

    profile = {
        "name": "search-query",
        "research_interests": list(
            {
                query.lower(),
                *query_tokens,
            }
        ),
        "skills": [],
    }

    agent = ExternalResearcherAgent()

    try:
        ranked = agent.find_matches(profile)
    except Exception:
        return []

    funding_calls = [
        {
            "id": funding.id,
            "name": funding.name,
            "organization": funding.organization,
            "deadline": funding.deadline,
            "fields": funding.fields or [],
            "keywords": funding.keywords or [],
        }
        for funding in db.query(FundingCall).all()
    ]

    mous = [
        {
            "id": mou.id,
            "institution": mou.institution,
            "country": mou.country,
            "status": mou.status,
        }
        for mou in db.query(MoU).all()
    ]

    results = []

    for entry in ranked[:top_k]:
        candidate = entry["candidate"]
        match_score = entry["match_score"]

        if match_score <= 0:
            continue

        combined_areas = set(
            candidate.get("research_interests") or []
        ) | set(
            candidate.get("skills") or []
        )

        funding_matches = (
            find_relevant_funding(
                combined_areas,
                funding_calls,
            )
            if combined_areas
            else []
        )

        mou_matches = find_relevant_mou(
            [
                candidate.get("institution"),
                candidate.get("country"),
            ],
            mous,
        )

        results.append(
            {
                "result_type": "external",

                "researcher": {
                    "id": candidate.get("id"),
                    "name": candidate.get("name"),
                    "institution": candidate.get("institution"),
                    "country": candidate.get("country"),
                },

                "score": round(match_score * 100, 1),

                "matching_expertise": (
                    candidate.get("research_interests") or []
                ),

                "skills": candidate.get("skills") or [],

                "research_area": candidate.get("research_area"),

                "funding_opportunities": [
                    {
                        "id": match.get("id"),
                        "name": match.get(
                            "title",
                            match.get("name"),
                        ),
                        "organization": match.get("organization"),
                    }
                    for match in funding_matches
                ],

                "mou_opportunities": [
                    {
                        "id": match.get("id"),
                        "institution": match.get(
                            "partner_institution",
                            match.get("institution"),
                        ),
                        "status": match.get("status"),
                    }
                    for match in mou_matches
                ],

                "reason": (
                    f"{candidate.get('name')} at "
                    f"{candidate.get('institution') or 'an external institution'} "
                    f"shares research interests with your query."
                ),
            }
        )

    return results


def unified_search(
    current_faculty_id: int,
    query: str,
    top_k: int = 10,
) -> list[dict]:
    """
    Single entry point behind the faculty search box.

    Existing matching engines are called here and their results are
    merged into one ranked response containing internal faculty and
    external researcher candidates.
    """
    query = query.strip()

    if not query:
        return []

    db = SessionLocal()

    try:
        # Existing internal faculty matching engine.
        internal = matching_service.search_collaborators(
            db,
            current_faculty_id,
            query,
            top_k=top_k,
        )

        # Existing collaboration graph/network algorithm.
        internal = _enrich_internal_with_network(
            db,
            current_faculty_id,
            internal,
        )

        # Existing external researcher matching engine.
        external = _external_results(
            db,
            query,
            top_k,
        )

        # Merge existing results without creating a new score.
        merged = internal + external

        # All existing result scores use a 0-100 display scale here.
        merged.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        # Return exactly the requested number of results.
        return merged[:top_k]

    finally:
        db.close()