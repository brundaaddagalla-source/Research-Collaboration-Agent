"""
Agent 24 - Collaboration Matching Engine
==========================================

Finds potential research collaboration opportunities between faculty.

The engine does NOT simply recommend researchers with similar embeddings.

Instead, it combines:

    Semantic similarity
        +
    Expertise complementarity
        +
    Publication/project evidence
        +
    Network reachability
        +
    Funding relevance
        +
    Institutional/MoU context

to answer:

    "Why could these researchers collaborate,
     and how promising is the opportunity?"

Embeddings are used mainly for candidate discovery.
The final opportunity score is based on multiple signals.
"""

import math
import re
from collections import deque
import os
import requests

from dotenv import load_dotenv

from services.embedding_service import get_embedding
from algorithms.collaboration_scoring import calculate_collaboration_score

load_dotenv()

FREELLMAPI_API_KEY = os.getenv(
    "FREELLMAPI_API_KEY"
)

FREELLMAPI_BASE_URL = os.getenv(
    "FREELLMAPI_BASE_URL",
    "http://127.0.0.1:31415/v1"
)

GEMINI_MODEL = "gemini-3.6-flash"


# ======================================================================
# EMBEDDING PRIMITIVES
# ======================================================================

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two embeddings.
    """

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def generate_embeddings(profiles):
    """
    Generate bge-m3 embeddings for faculty profiles.

    Embeddings are used to discover potentially related
    candidates. They are NOT the final collaboration score.
    """

    embeddings = []

    for faculty in profiles:

        print(
            f"Generating embedding for: "
            f"{faculty['name']}"
        )

        embedding = get_embedding(
            faculty["profile"]
        )

        embeddings.append(
            {
                "faculty_id": faculty["faculty_id"],
                "name": faculty["name"],
                "department": faculty["department"],
                "profile": faculty["profile"],
                "embedding": embedding,
            }
        )

    return embeddings


def _lookup_embedding(
    embeddings,
    name,
):
    """
    Find an embedding by faculty name.
    """

    for faculty in embeddings:

        if faculty["name"] == name:
            return faculty["embedding"]

    return None


# ======================================================================
# RESEARCH AREA EXTRACTION
# ======================================================================

def extract_research_areas(profile):
    """
    Extract self-declared research areas from a faculty profile.
    """

    for line in profile.splitlines():

        if line.startswith("Research Areas:"):

            areas = line.replace(
                "Research Areas:",
                "",
                1,
            ).strip()

            if not areas:
                return []

            return [
                area.strip().lower()
                for area in areas.split(",")
                if area.strip()
            ]

    return []


# ======================================================================
# TEXT / EVIDENCE HELPERS
# ======================================================================

def _tokenize_text(text):
    """
    Convert text into simple normalized tokens.

    This is intentionally lightweight.

    We do not want a huge manually-maintained research
    dictionary at this stage.
    """

    if not text:
        return set()

    words = re.findall(
        r"[a-zA-Z0-9]+",
        str(text).lower(),
    )

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "using",
        "based",
        "analysis",
        "approach",
        "methods",
        "method",
        "system",
        "development",
        "data",
        "research",
        "study",
        "model",
        "models",
        "of",
        "in",
        "to",
        "on",
        "a",
        "an",
    }

    return {
        word
        for word in words
        if word not in stop_words
        and len(word) > 2
    }


def _normalize_area(area):
    """
    Normalize a research-area string.
    """

    if not area:
        return ""

    return str(area).strip().lower()


def _get_keywords_from_item(item):
    """
    Extract evidence keywords from either:

    1. Explicit keywords, if supplied.
    2. Current Agent 24 database fields.

    This allows the function to work with both the current
    prototype data and future richer schemas.
    """

    keywords = set()

    # --------------------------------------------------------------
    # Explicit keywords
    # --------------------------------------------------------------

    for keyword in item.get("keywords") or []:

        normalized = _normalize_area(keyword)

        if normalized:
            keywords.add(normalized)

    # --------------------------------------------------------------
    # Research area
    # --------------------------------------------------------------

    research_area = item.get("research_area")

    if research_area:

        keywords.update(
            _tokenize_text(research_area)
        )

    # --------------------------------------------------------------
    # Title
    # --------------------------------------------------------------

    title = item.get("title")

    if title:

        keywords.update(
            _tokenize_text(title)
        )

    # --------------------------------------------------------------
    # Description
    # --------------------------------------------------------------

    description = item.get("description")

    if description:

        keywords.update(
            _tokenize_text(description)
        )

    return keywords


# ======================================================================
# EVIDENCE LAYER
# ======================================================================

# def build_expertise_evidence(
#     faculty_id,
#     research_areas=None,
#     publications=None,
#     projects=None,
# ):
#     """
#     Build evidence of what a faculty member actually works on.

#     Uses the CURRENT Agent 24 data structure:

#         Faculty.research_areas

#         Publication:
#             title
#             year
#             venue
#             doi

#         Project:
#             title
#             description
#             research_area
#             status

#     No keywords column is required.

#     Research areas provide declared expertise.

#     Publications and projects provide demonstrated expertise.
#     """

#     research_areas = research_areas or []
#     publications = publications or []
#     projects = projects or []

#     declared_areas = {
#         _normalize_area(area)
#         for area in research_areas
#         if _normalize_area(area)
#     }

#     publication_keywords = set()

#     recent_publications = []

#     for publication in publications:

#         publication_keywords.update(
#             _get_keywords_from_item(
#                 publication
#             )
#         )

#         recent_publications.append(
#             (
#                 publication.get("year") or 0,
#                 publication.get("title"),
#             )
#         )

#     project_keywords = set()

#     active_projects = []

#     for project in projects:

#         project_keywords.update(
#             _get_keywords_from_item(
#                 project
#             )
#         )

#         status = str(
#             project.get("status") or ""
#         ).lower()

#         if status in {
#             "ongoing",
#             "proposed",
#             "active",
#         }:

#             active_projects.append(
#                 project.get("title")
#             )

#     recent_publications.sort(
#         key=lambda item: item[0],
#         reverse=True,
#     )

#     # --------------------------------------------------------------
#     # Evidence strength
#     # --------------------------------------------------------------

#     publication_count = len(
#         publications
#     )

#     project_count = len(
#         projects
#     )

#     evidence_strength = calculate_evidence_strength(
#         publication_count,
#         project_count,
#     )

#     # --------------------------------------------------------------
#     # Combined evidence
#     # --------------------------------------------------------------

#     combined_keywords = (
#         declared_areas
#         |
#         publication_keywords
#         |
#         project_keywords
#     )

#     return {
#         "faculty_id": faculty_id,

#         "declared_areas": declared_areas,

#         "publication_keywords": publication_keywords,

#         "project_keywords": project_keywords,

#         "combined_keywords": combined_keywords,

#         "publication_count": publication_count,

#         "project_count": project_count,

#         "recent_publications": [
#             title
#             for _, title in recent_publications[:3]
#             if title
#         ],

#         "active_projects": [
#             title
#             for title in active_projects
#             if title
#         ],

#         "evidence_strength": evidence_strength,
#     }

def build_expertise_evidence(
    faculty_id,
    research_areas=None,
    publications=None,
    projects=None,
):
    """
    Build evidence of what a faculty member actually works on.

    Uses the CURRENT Agent 24 data structure:

        Faculty.research_areas

        Publication:
            title
            year
            venue
            doi

        Project:
            title
            description
            research_area
            status

    Research areas provide declared expertise.

    Publications and projects provide demonstrated
    expertise.

    Keyword sets are retained for the existing matching
    algorithm, while structured evidence is also retained
    for explanations and LLM-generated collaboration briefs.
    """

    research_areas = research_areas or []
    publications = publications or []
    projects = projects or []

    # --------------------------------------------------------------
    # Declared research areas
    # --------------------------------------------------------------

    declared_areas = {
        _normalize_area(area)
        for area in research_areas
        if _normalize_area(area)
    }

    # --------------------------------------------------------------
    # Publication evidence
    # --------------------------------------------------------------

    publication_keywords = set()
    recent_publications = []
    publication_details = []

    for publication in publications:

        publication_keywords.update(
            _get_keywords_from_item(
                publication
            )
        )

        title = publication.get(
            "title"
        )

        year = (
            publication.get("year")
            or 0
        )

        recent_publications.append(
            (
                year,
                title,
            )
        )

        if title:
            publication_details.append(
                {
                    "title": title,
                    "year": year,
                    "venue": publication.get(
                        "venue"
                    ),
                    "doi": publication.get(
                        "doi"
                    ),
                }
            )

    # --------------------------------------------------------------
    # Project evidence
    # --------------------------------------------------------------

    project_keywords = set()
    active_projects = []
    project_details = []

    for project in projects:

        project_keywords.update(
            _get_keywords_from_item(
                project
            )
        )

        title = project.get(
            "title"
        )

        description = project.get(
            "description"
        )

        research_area = project.get(
            "research_area"
        )

        status = str(
            project.get("status") or ""
        ).lower()

        project_details.append(
            {
                "title": title,
                "description": description,
                "research_area":
                    research_area,
                "status":
                    project.get("status"),
            }
        )

        if status in {
            "ongoing",
            "proposed",
            "active",
        }:

            if title:
                active_projects.append(
                    title
                )

    # --------------------------------------------------------------
    # Sort publications by year
    # --------------------------------------------------------------

    recent_publications.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    # --------------------------------------------------------------
    # Evidence strength
    # --------------------------------------------------------------

    publication_count = len(
        publications
    )

    project_count = len(
        projects
    )

    evidence_strength = (
        calculate_evidence_strength(
            publication_count,
            project_count,
        )
    )

    # --------------------------------------------------------------
    # Combined evidence
    # --------------------------------------------------------------

    combined_keywords = (
        declared_areas
        |
        publication_keywords
        |
        project_keywords
    )

    # --------------------------------------------------------------
    # Return structured evidence
    # --------------------------------------------------------------

    return {
        "faculty_id":
            faculty_id,

        "declared_areas":
            declared_areas,

        "research_areas":
            list(declared_areas),

        "publication_keywords":
            publication_keywords,

        "project_keywords":
            project_keywords,

        "combined_keywords":
            combined_keywords,

        "publication_count":
            publication_count,

        "project_count":
            project_count,

        "recent_publications": [
            title
            for _, title in recent_publications[:3]
            if title
        ],

        "active_projects": [
            title
            for title in active_projects
            if title
        ],

        "evidence_strength":
            evidence_strength,

        # New structured evidence
        "publication_details":
            publication_details,

        "project_details":
            project_details,
    }


def calculate_evidence_strength(
    publication_count,
    project_count,
):
    """
    Estimate how strongly the faculty member's
    expertise is supported by actual research activity.

    This is NOT a measure of researcher quality.

    It only answers:

        "How much evidence do we have?"
    """

    score = 0.0

    if publication_count > 0:
        score += min(
            publication_count / 5,
            1.0,
        ) * 0.60

    if project_count > 0:
        score += min(
            project_count / 3,
            1.0,
        ) * 0.40

    return round(
        min(score, 1.0),
        4,
    )


# ======================================================================
# NETWORK LAYER
# ======================================================================

# def build_collaboration_graph(
#     collaborations,
# ):
#     """
#     Build an undirected collaboration graph.

#     Current database stores faculty names:
#         faculty_a
#         faculty_b

#     The matching engine internally uses faculty IDs,
#     so the names are converted using the supplied faculty data.
#     """

#     graph = {}

#     for collaboration in collaborations:

#         faculty_a = collaboration["faculty_a_id"]
#         faculty_b = collaboration["faculty_b_id"]

#         graph.setdefault(
#             faculty_a,
#             set(),
#         ).add(faculty_b)

#         graph.setdefault(
#             faculty_b,
#             set(),
#         ).add(faculty_a)

#     return graph

def build_collaboration_graph(
    collaborations,
):
    """
    Build an undirected collaboration graph.

    Supports both:

        faculty_a_id / faculty_b_id

    and the current database fields:

        faculty_a / faculty_b
    """

    graph = {}

    for collaboration in collaborations:

        faculty_a = (
            collaboration.get(
                "faculty_a_id"
            )
            if collaboration.get(
                "faculty_a_id"
            ) is not None
            else collaboration.get(
                "faculty_a"
            )
        )

        faculty_b = (
            collaboration.get(
                "faculty_b_id"
            )
            if collaboration.get(
                "faculty_b_id"
            ) is not None
            else collaboration.get(
                "faculty_b"
            )
        )

        if faculty_a is None or faculty_b is None:
            continue

        graph.setdefault(
            faculty_a,
            set(),
        ).add(faculty_b)

        graph.setdefault(
            faculty_b,
            set(),
        ).add(faculty_a)

    return graph


def network_distance(
    graph,
    faculty_a_id,
    faculty_b_id,
    max_hops=4,
):
    """
    Find shortest path between two faculty members.

    Returns:

        0    same person
        1    direct collaborators
        2    one intermediary
        3    two intermediaries
        None no known path
    """

    if faculty_a_id == faculty_b_id:
        return 0

    if (
        faculty_a_id not in graph
        or faculty_b_id not in graph
    ):
        return None

    visited = {
        faculty_a_id
    }

    queue = deque(
        [
            (
                faculty_a_id,
                0,
            )
        ]
    )

    while queue:

        node, distance = queue.popleft()

        if distance >= max_hops:
            continue

        for neighbor in graph.get(
            node,
            (),
        ):

            if neighbor == faculty_b_id:

                return distance + 1

            if neighbor not in visited:

                visited.add(neighbor)

                queue.append(
                    (
                        neighbor,
                        distance + 1,
                    )
                )

    return None


def reachability_label(distance):
    """
    Convert network distance into readable text.
    """

    if distance is None:
        return "No known path"

    if distance == 0:
        return "Same researcher"

    if distance == 1:
        return "Direct collaborators"

    if distance == 2:
        return "One connection away"

    if distance <= 4:
        return (
            f"{distance - 1} connections away"
        )

    return "Distant"


def calculate_network_score(distance):
    """
    Convert network distance into a normalized score.

    Important:

    A missing network path does NOT mean the collaboration
    is bad.

    It simply means there is no known route through the
    current collaboration network.

    Therefore isolated researchers receive a neutral score.
    """

    if distance is None:
        return 0.50

    if distance == 1:
        return 0.90

    if distance == 2:
        return 0.80

    if distance == 3:
        return 0.65

    if distance == 4:
        return 0.50

    return 0.40


# ======================================================================
# EXISTING COLLABORATION FILTER
# ======================================================================

def normalize_pair(
    faculty_a_id,
    faculty_b_id,
):
    """
    Create a consistent representation of a faculty pair.
    """

    return tuple(
        sorted(
            [
                faculty_a_id,
                faculty_b_id,
            ]
        )
    )


def get_existing_collaboration_pairs(
    collaborations,
):
    """
    Return all existing faculty collaboration pairs.
    """

    pairs = set()

    for collaboration in collaborations:

        pairs.add(
            normalize_pair(
                collaboration["faculty_a_id"],
                collaboration["faculty_b_id"],
            )
        )

    return pairs


def already_collaborating(
    faculty_a_id,
    faculty_b_id,
    collaborations,
):
    """
    Check whether two faculty members already collaborate.
    """

    existing_pairs = (
        get_existing_collaboration_pairs(
            collaborations
        )
    )

    return (
        normalize_pair(
            faculty_a_id,
            faculty_b_id,
        )
        in existing_pairs
    )


# ======================================================================
# COMPLEMENTARITY
# ======================================================================

def calculate_complementarity(
    areas_a,
    areas_b,
    semantic_similarity=0,
):
    """
    Estimate expertise complementarity.

    Important distinction:

        Similarity:
            How related are the two profiles?

        Complementarity:
            How much useful DIFFERENT expertise can they
            bring to the same research direction?

    Shared expertise alone is therefore not enough.
    """

    areas_a = {
        str(area).lower().strip()
        for area in areas_a
        if str(area).strip()
    }

    areas_b = {
        str(area).lower().strip()
        for area in areas_b
        if str(area).strip()
    }

    if not areas_a or not areas_b:
        return 0.0

    overlap = (
        areas_a.intersection(
            areas_b
        )
    )

    unique_a = (
        areas_a - overlap
    )

    unique_b = (
        areas_b - overlap
    )

    # --------------------------------------------------------------
    # Same expertise
    # --------------------------------------------------------------

    if areas_a == areas_b:

        return 0.40

    # --------------------------------------------------------------
    # Shared foundation + different expertise
    # --------------------------------------------------------------

    if (
        overlap
        and unique_a
        and unique_b
    ):

        semantic_component = min(
            max(
                semantic_similarity,
                0.0,
            ),
            1.0,
        )

        difference_component = min(
            (
                len(unique_a)
                + len(unique_b)
            ) / 4,
            1.0,
        )

        score = (
            0.55 * semantic_component
            +
            0.45 * difference_component
        )

        return round(
            score,
            4,
        )

    # --------------------------------------------------------------
    # One expertise set contains the other
    # --------------------------------------------------------------

    if overlap and (
        not unique_a
        or not unique_b
    ):

        return round(
            0.45
            +
            (
                semantic_similarity
                * 0.20
            ),
            4,
        )

    # --------------------------------------------------------------
    # No direct overlap
    # --------------------------------------------------------------
    #
    # There may still be a useful interdisciplinary relationship.
    #

    semantic_component = min(
        max(
            semantic_similarity,
            0.0,
        ),
        1.0,
    )

    if semantic_component < 0.55:
        return 0.30

    return round(
        0.30
        +
        (
            semantic_component
            * 0.55
        ),
        4,
    )


# ======================================================================
# RESEARCH EVIDENCE RELEVANCE
# ======================================================================

# def calculate_evidence_relevance(
#     evidence_a,
#     evidence_b,
# ):
#     """
#     Estimate how strongly the two faculty members have
#     demonstrated relevant research activity.

#     This combines:

#         publication evidence
#         project evidence
#         active project evidence
#     """

#     evidence_a_strength = (
#         evidence_a.get(
#             "evidence_strength",
#             0.0,
#         )
#     )

#     evidence_b_strength = (
#         evidence_b.get(
#             "evidence_strength",
#             0.0,
#         )
#     )

#     average_strength = (
#         evidence_a_strength
#         +
#         evidence_b_strength
#     ) / 2

#     active_project_bonus = 0.0

#     if evidence_a.get(
#         "active_projects"
#     ):
#         active_project_bonus += 0.10

#     if evidence_b.get(
#         "active_projects"
#     ):
#         active_project_bonus += 0.10

#     return round(
#         min(
#             average_strength
#             +
#             active_project_bonus,
#             1.0,
#         ),
#         4,
#     )

def calculate_evidence_relevance(
    evidence_a,
    evidence_b,
    shared_topics=None,
):
    """
    Estimate how strongly the collaboration is supported
    by demonstrated research activity.

    Evidence includes:
        - publication activity
        - project activity
        - active projects
        - overlap with the proposed research direction

    Missing evidence is not automatically treated as negative.
    """

    shared_topics = set(shared_topics or [])

    evidence_a_strength = evidence_a.get(
        "evidence_strength",
        0.0,
    )

    evidence_b_strength = evidence_b.get(
        "evidence_strength",
        0.0,
    )

    average_strength = (
        evidence_a_strength
        + evidence_b_strength
    ) / 2

    activity_bonus = 0.0

    if evidence_a.get("publication_count", 0) > 0:
        activity_bonus += 0.05

    if evidence_b.get("publication_count", 0) > 0:
        activity_bonus += 0.05

    if evidence_a.get("active_projects"):
        activity_bonus += 0.05

    if evidence_b.get("active_projects"):
        activity_bonus += 0.05

    combined_a = set(
        evidence_a.get(
            "combined_keywords",
            set(),
        )
    )

    combined_b = set(
        evidence_b.get(
            "combined_keywords",
            set(),
        )
    )

    relevance_bonus = 0.0

    if shared_topics:
        evidence_overlap = (
            combined_a
            & combined_b
            & shared_topics
        )

        if evidence_overlap:
            relevance_bonus = min(
                len(evidence_overlap) * 0.05,
                0.15,
            )

    score = (
        average_strength
        + activity_bonus
        + relevance_bonus
    )

    return round(
        min(max(score, 0.0), 1.0),
        4,
    )

# ======================================================================
# FUNDING
# ======================================================================

# def find_relevant_funding(
#     combined_areas,
#     funding_calls,
# ):
#     """
#     Find funding calls whose declared research areas
#     overlap the combined research evidence.

#     This is an initial deterministic matcher.

#     Semantic funding matching can be added later.
#     """

#     combined_areas = {
#         str(area).lower().strip()
#         for area in combined_areas
#         if str(area).strip()
#     }

#     matches = []

#     for call in funding_calls:

#         call_areas = {
#             str(area).lower().strip()
#             for area in (
#                 call.get(
#                     "research_areas"
#                 )
#                 or []
#             )
#             if str(area).strip()
#         }

#         overlap = (
#             combined_areas
#             &
#             call_areas
#         )

#         if overlap:

#             matches.append(
#                 {
#                     "id": call.get("id"),
#                     "title": call.get("title"),
#                     "organization": call.get(
#                         "organization"
#                     ),
#                     "deadline": call.get(
#                         "deadline"
#                     ),
#                     "matched_areas": sorted(
#                         overlap
#                     ),
#                 }
#             )

#     return matches

GENERIC_FUNDING_TERMS = {
    "learning",
    "deep",
    "intelligence",
    "machine",

    "system",
    "systems",

    "application",
    "applications",

    "analysis",
    "analyses",

    "method",
    "methods",

    "research",

    "technology",
    "technologies",

    "computer",
    "computing",

    "artificial",

    "data",
    "based",
}

def find_relevant_funding(
    combined_areas,
    funding_calls,
):
    """
    Find funding calls relevant to the combined research
    evidence of two faculty members.

    Supports the current Agent 24 database schema:

        FundingCall.name
        FundingCall.fields
        FundingCall.keywords
    """

    combined_areas = {
        str(area).lower().strip()
        for area in combined_areas
        if str(area).strip()
    }

    matches = []

    for call in funding_calls:
        call_terms = set()

        fields = call.get("fields") or []
        keywords = call.get("keywords") or []

        if isinstance(fields, str):
            fields = [fields]

        if isinstance(keywords, str):
            keywords = [keywords]

        for field in fields:
            call_terms.update(
                _tokenize_text(field)
            )

        for keyword in keywords:
            call_terms.update(
                _tokenize_text(keyword)
            )

        overlap = (
            combined_areas
            & call_terms
        )

        meaningful_overlap = {
            term
            for term in overlap
            if term not in GENERIC_FUNDING_TERMS
        }

        if meaningful_overlap:
            matches.append(
                {
                    "id": call.get("id"),
                    "title": call.get("name"),
                    "organization": call.get(
                        "organization"
                    ),
                    "deadline": call.get(
                        "deadline"
                    ),
                    "matched_areas": sorted(
                        meaningful_overlap
                    ),
                }
            )

    return matches


def calculate_funding_score(
    funding_matches,
):
    """
    Convert funding matches into a normalized score.
    """

    if not funding_matches:
        return 0.30

    if len(funding_matches) >= 2:
        return 1.0

    return 0.85


# ======================================================================
# MOU
# ======================================================================

# def find_relevant_mou(
#     countries_or_institutions,
#     mous,
# ):
#     """
#     Find MoUs matching supplied institutions/countries.

#     Mainly useful for external collaboration candidates.
#     """

#     targets = {
#         str(target).lower().strip()
#         for target in countries_or_institutions
#         if target
#     }

#     matches = []

#     for mou in mous:

#         institution = str(
#             mou.get(
#                 "partner_institution"
#             )
#             or ""
#         ).lower()

#         country = str(
#             mou.get(
#                 "country"
#             )
#             or ""
#         ).lower()

#         if (
#             institution in targets
#             or country in targets
#         ):

#             matches.append(
#                 {
#                     "id": mou.get("id"),
#                     "partner_institution":
#                         mou.get(
#                             "partner_institution"
#                         ),
#                     "status":
#                         mou.get("status"),
#                 }
#             )

#     return matches

def find_relevant_mou(
    countries_or_institutions,
    mous,
):
    """
    Find MoUs matching supplied institutions or countries.

    Supports the current Agent 24 database schema:

        MoU.institution
        MoU.country
        MoU.status
    """

    targets = {
        str(target).lower().strip()
        for target in countries_or_institutions
        if str(target).strip()
    }

    matches = []

    for mou in mous:
        institution = str(
            mou.get("institution")
            or ""
        ).lower().strip()

        country = str(
            mou.get("country")
            or ""
        ).lower().strip()

        if (
            institution in targets
            or country in targets
        ):
            matches.append(
                {
                    "id": mou.get("id"),
                    "partner_institution":
                        mou.get("institution"),
                    "country":
                        mou.get("country"),
                    "status":
                        mou.get("status"),
                }
            )

    return matches


def calculate_mou_score(
    mou_matches,
):
    """
    MoU opportunity score.

    No MoU is neutral rather than negative.
    """

    if not mou_matches:
        return 0.50

    return 0.90



def generate_llm_collaboration_explanation(
    faculty_a,
    faculty_b,
    evidence_a,
    evidence_b,
    opportunity,
):
    """
    Generate a human-readable collaboration explanation
    using Gemini.

    Gemini only explains the already-computed opportunity.
    It does not calculate or modify the collaboration score.
    """

    if not FREELLMAPI_API_KEY:
        return None

    prompt = f"""
You are a research collaboration advisor.

Explain why the following two researchers could collaborate.

IMPORTANT RULES:
- Use ONLY the information provided below.
- Do NOT invent research areas, publications, projects,
  funding opportunities, institutions, or achievements.
- Do NOT change or reinterpret the numerical collaboration score.
- Do NOT claim that the researchers already collaborate.
- The goal is to identify a NEW potential collaboration.
- Be specific and evidence-based.
- Keep the explanation concise and professional.

RESEARCHER A
Name: {faculty_a.get("name")}
Department: {faculty_a.get("department")}
Research areas: {evidence_a.get("research_areas")}
Publications: {evidence_a.get("publication_details")}
Projects: {evidence_a.get("project_details")}

RESEARCHER B
Name: {faculty_b.get("name")}
Department: {faculty_b.get("department")}
Research areas: {evidence_b.get("research_areas")}
Publications: {evidence_b.get("publication_details")}
Projects: {evidence_b.get("project_details")}

COLLABORATION ANALYSIS
Potential topic: {opportunity.get("potential_topic")}
Shared topics: {opportunity.get("shared_topics")}
Researcher A unique contribution:
{opportunity.get("unique_contribution_a")}

Researcher B unique contribution:
{opportunity.get("unique_contribution_b")}

Semantic similarity:
{opportunity.get("semantic_similarity")}

Complementarity:
{opportunity.get("complementarity_score")}

Evidence relevance:
{opportunity.get("evidence_relevance")}

Network reachability:
{opportunity.get("network_reachability")}

Funding opportunities:
{opportunity.get("funding_opportunities")}

Final collaboration score:
{opportunity.get("collaboration_score")}

Return exactly these sections:

Potential Research Topic:

Researcher A Contribution:

Researcher B Contribution:

Why This Collaboration Makes Sense:

Evidence:

Funding Relevance:
"""

    try:
        response = requests.post(
            f"{FREELLMAPI_BASE_URL}/chat/completions",
            headers={
                "Authorization":
                    f"Bearer {FREELLMAPI_API_KEY}",
                "Content-Type":
                    "application/json",
            },
            json={
                "model": GEMINI_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
            timeout=120,
        )

        if response.status_code != 200:
            print(
                "LLM API failed:",
                response.status_code,
                response.text
            )
            return None

        result = response.json()

        return (
            result["choices"][0]["message"]["content"]
        )

    except Exception as e:
        print("LLM explanation failed:", e)
        return None


# def generate_potential_topic(
#     faculty_a,
#     faculty_b,
#     evidence_a,
#     evidence_b,
# ):
#     """
#     Generate a deterministic research topic from
#     meaningful research areas and project evidence.

#     This provides a fallback topic before the
#     LLM explanation layer.
#     """

#     research_areas_a = [
#         str(area).strip()
#         for area in evidence_a.get(
#             "research_areas",
#             []
#         )
#         if str(area).strip()
#     ]

#     research_areas_b = [
#         str(area).strip()
#         for area in evidence_b.get(
#             "research_areas",
#             []
#         )
#         if str(area).strip()
#     ]

#     project_a = (
#         evidence_a.get(
#             "active_projects",
#             []
#         )
#     )

#     project_b = (
#         evidence_b.get(
#             "active_projects",
#             []
#         )
#     )

#     # --------------------------------------------------
#     # Shared research areas
#     # --------------------------------------------------

#     shared_areas = []

#     for area_a in research_areas_a:
#         for area_b in research_areas_b:

#             if area_a.lower() == area_b.lower():

#                 shared_areas.append(
#                     area_a
#                 )

#     # --------------------------------------------------
#     # Prefer different expertise
#     # --------------------------------------------------

#     unique_areas_a = [
#         area
#         for area in research_areas_a
#         if area.lower()
#         not in {
#             item.lower()
#             for item in research_areas_b
#         }
#     ]

#     unique_areas_b = [
#         area
#         for area in research_areas_b
#         if area.lower()
#         not in {
#             item.lower()
#             for item in research_areas_a
#         }
#     ]

#     if unique_areas_a and unique_areas_b:

#         return (
#             "Interdisciplinary research combining "
#             f"{unique_areas_a[0]} and "
#             f"{unique_areas_b[0]}"
#         )

#     # --------------------------------------------------
#     # Shared research direction
#     # --------------------------------------------------

#     if shared_areas:

#         return (
#             f"Joint research in "
#             f"{shared_areas[0]}"
#         )

#     # --------------------------------------------------
#     # Project-based fallback
#     # --------------------------------------------------

#     if project_a and project_b:

#         return (
#             "Interdisciplinary research connecting "
#             f"{project_a[0]} and "
#             f"{project_b[0]}"
#         )

#     return (
#         "Exploratory interdisciplinary research"
#     )

def generate_potential_topic(
    faculty_a,
    faculty_b,
    evidence_a,
    evidence_b,
):
    """
    Generate a deterministic, evidence-based research topic.

    Preference order:

        1. Shared research area + unique expertise
        2. Unique expertise from both researchers
        3. Active project combination
        4. Shared research area
        5. Exploratory fallback
    """

    research_areas_a = [
        str(area).strip()
        for area in evidence_a.get(
            "research_areas",
            [],
        )
        if str(area).strip()
    ]

    research_areas_b = [
        str(area).strip()
        for area in evidence_b.get(
            "research_areas",
            [],
        )
        if str(area).strip()
    ]

    project_a = (
        evidence_a.get(
            "active_projects",
            [],
        )
    )

    project_b = (
        evidence_b.get(
            "active_projects",
            [],
        )
    )

    areas_a_lower = {
        area.lower()
        for area in research_areas_a
    }

    areas_b_lower = {
        area.lower()
        for area in research_areas_b
    }

    shared_areas = [
        area
        for area in research_areas_a
        if area.lower() in areas_b_lower
    ]

    unique_areas_a = [
        area
        for area in research_areas_a
        if area.lower() not in areas_b_lower
    ]

    unique_areas_b = [
        area
        for area in research_areas_b
        if area.lower() not in areas_a_lower
    ]

    # --------------------------------------------------------------
    # Shared foundation + complementary expertise
    # --------------------------------------------------------------

    if (
        shared_areas
        and unique_areas_a
        and unique_areas_b
    ):
        return (
            f"{shared_areas[0]} research combining "
            f"{unique_areas_a[0]} and "
            f"{unique_areas_b[0]}"
        )

    # --------------------------------------------------------------
    # Complementary expertise without shared declared area
    # --------------------------------------------------------------

    if unique_areas_a and unique_areas_b:
        return (
            "Interdisciplinary research combining "
            f"{unique_areas_a[0]} and "
            f"{unique_areas_b[0]}"
        )

    # --------------------------------------------------------------
    # Project-based topic
    # --------------------------------------------------------------

    if project_a and project_b:
        return (
            "Joint research connecting "
            f"{project_a[0]} and "
            f"{project_b[0]}"
        )

    # --------------------------------------------------------------
    # Shared research area
    # --------------------------------------------------------------

    if shared_areas:
        return (
            f"Joint research in "
            f"{shared_areas[0]}"
        )

    return (
        "Exploratory interdisciplinary research"
    )


# ======================================================================
# FINAL COLLABORATION SCORE
# ======================================================================

# def calculate_collaboration_score(
#     complementarity_score,
#     semantic_similarity,
#     evidence_relevance,
#     network_score,
#     funding_score,
#     mou_score,
# ):
#     """
#     Calculate the overall collaboration opportunity score.

#     Internal collaboration weighting:

#         30% Complementarity
#         25% Research relevance
#         15% Project/evidence relevance
#         15% Network reachability
#         10% Funding compatibility
#          5% Institutional/MoU relationship
#     """

#     score = (
#         0.30 * complementarity_score
#         +
#         0.25 * semantic_similarity
#         +
#         0.15 * evidence_relevance
#         +
#         0.15 * network_score
#         +
#         0.10 * funding_score
#         +
#         0.05 * mou_score
#     )

#     return round(
#         min(
#             max(score, 0.0),
#             1.0,
#         ),
#         4,
#     )




# ======================================================================
# COLLABORATION HYPOTHESIS
# ======================================================================

def generate_collaboration_hypothesis(
    faculty_a,
    faculty_b,
    evidence_a,
    evidence_b,
    semantic_similarity,
    complementarity,
    graph,
    funding_calls,
    mous=None,
):
    """
    Generate an evidence-based collaboration opportunity.
    """

    shared_topics = sorted(
        evidence_a["combined_keywords"]
        &
        evidence_b["combined_keywords"]
    )

    unique_a = sorted(
        evidence_a["combined_keywords"]
        -
        evidence_b["combined_keywords"]
    )

    unique_b = sorted(
        evidence_b["combined_keywords"]
        -
        evidence_a["combined_keywords"]
    )

    combined_areas = (
        evidence_a["combined_keywords"]
        |
        evidence_b["combined_keywords"]
    )

    distance = network_distance(
        graph,
        faculty_a["faculty_id"],
        faculty_b["faculty_id"],
    )

    network_score = calculate_network_score(
        distance
    )

    funding_matches = find_relevant_funding(
        combined_areas,
        funding_calls,
    )

    funding_score = calculate_funding_score(
        funding_matches
    )

    mou_matches = []

    if faculty_b.get(
        "institution"
    ):

        mou_matches = find_relevant_mou(
            [
                faculty_b.get(
                    "institution"
                )
            ],
            mous or [],
        )

    mou_score = calculate_mou_score(
        mou_matches
    )

    evidence_relevance = (
        calculate_evidence_relevance(
            evidence_a,
            evidence_b,
            shared_topics=shared_topics,
        )
    )

    collaboration_score = (
        calculate_collaboration_score(
            complementarity_score=
                complementarity,

            research_relevance_score=
                semantic_similarity,

            evidence_score=
                evidence_relevance,

            network_score=
                network_score,

            funding_score=
                funding_score,

            mou_score=
                mou_score,
        )
    )

    potential_topic = (
        generate_potential_topic(
            faculty_a,
            faculty_b,
            evidence_a,
            evidence_b,
        )
    )

    reasons = []

    # --------------------------------------------------------------
    # Research relationship
    # --------------------------------------------------------------

    if shared_topics:

        reasons.append(
            "Both researchers have evidence "
            "connected to "
            +
            ", ".join(
                shared_topics[:3]
            )
            +
            "."
        )

    # --------------------------------------------------------------
    # Complementary expertise
    # --------------------------------------------------------------

    if unique_a and unique_b:

        reasons.append(
            f"{faculty_a['name']} contributes "
            f"{', '.join(unique_a[:3])}, "
            f"while {faculty_b['name']} contributes "
            f"{', '.join(unique_b[:3])}."
        )

    # --------------------------------------------------------------
    # Publication/project evidence
    # --------------------------------------------------------------

    if (
        evidence_a["publication_count"]
        or
        evidence_b["publication_count"]
    ):

        reasons.append(
            "The collaboration is supported by "
            "publication evidence from the researchers."
        )

    if (
        evidence_a["active_projects"]
        or
        evidence_b["active_projects"]
    ):

        active_projects = (
            evidence_a["active_projects"][:1]
            +
            evidence_b["active_projects"][:1]
        )

        reasons.append(
            "Active project work provides "
            "a potential starting point: "
            +
            ", ".join(
                active_projects
            )
            +
            "."
        )

    # --------------------------------------------------------------
    # Network
    # --------------------------------------------------------------

    if distance is None:

        reasons.append(
            "No existing path was found between "
            "the researchers in the collaboration "
            "network, indicating a new connection."
        )

    elif distance > 1:

        reasons.append(
            "The researchers are not direct "
            "collaborators and can potentially "
            "be connected through the existing "
            "research network."
        )

    # --------------------------------------------------------------
    # Funding
    # --------------------------------------------------------------

    if funding_matches:

        call = funding_matches[0]

        reasons.append(
            f"The research combination matches "
            f"the funding opportunity "
            f"'{call['title']}'."
        )

    # --------------------------------------------------------------
    # MoU
    # --------------------------------------------------------------

    if mou_matches:

        mou = mou_matches[0]

        reasons.append(
            "An existing institutional MoU may "
            f"support collaboration with "
            f"{mou['partner_institution']}."
        )

    if not reasons:

        reasons.append(
            "Limited evidence is currently "
            "available. Treat this as an "
            "exploratory opportunity."
        )

            # --------------------------------------------------------------
    # LLM explanation
    # --------------------------------------------------------------

    llm_explanation = (
        generate_llm_collaboration_explanation(
            faculty_a=faculty_a,
            faculty_b=faculty_b,
            evidence_a=evidence_a,
            evidence_b=evidence_b,
            opportunity={
                "potential_topic":
                    potential_topic,

                "shared_topics":
                    shared_topics,

                "unique_contribution_a":
                    unique_a,

                "unique_contribution_b":
                    unique_b,

                "semantic_similarity":
                    round(
                        semantic_similarity,
                        4,
                    ),

                "complementarity_score":
                    round(
                        complementarity,
                        4,
                    ),

                "evidence_relevance":
                    round(
                        evidence_relevance,
                        4,
                    ),

                    "network_reachability":
                        reachability_label(
                            distance
                        ),

                "funding_opportunities":
                    funding_matches,

                "collaboration_score":
                    collaboration_score,
            },
        )
    )

    return {
        "faculty_a": faculty_a["name"],
        "faculty_b": faculty_b["name"],

        "department_a":
            faculty_a["department"],

        "department_b":
            faculty_b["department"],

        "potential_topic":
            potential_topic,

        "semantic_similarity":
            round(
                semantic_similarity,
                4,
            ),

        "complementarity_score":
            round(
                complementarity,
                4,
            ),

        "evidence_relevance":
            round(
                evidence_relevance,
                4,
            ),

        "network_score":
            round(
                network_score,
                4,
            ),

        "funding_score":
            round(
                funding_score,
                4,
            ),

        "mou_score":
            round(
                mou_score,
                4,
            ),

        "collaboration_score":
            collaboration_score,

        "network_reachability":
            reachability_label(
                distance
            ),

        "shared_topics":
            shared_topics[:10],

        "unique_contribution_a":
            unique_a[:10],

        "unique_contribution_b":
            unique_b[:10],

        "funding_opportunities":
            funding_matches,

        "mou_opportunities":
            mou_matches,

        "reasons":
            reasons,

        "llm_explanation":
            llm_explanation,
    }




# ======================================================================
# SEMANTIC DISCOVERY
# ======================================================================

def find_similar_faculty(
    embeddings,
    faculty_name,
    top_k=5,
):
    """
    Find semantically similar faculty.

    This is only candidate discovery.
    """

    target_embedding = _lookup_embedding(
        embeddings,
        faculty_name,
    )

    if target_embedding is None:
        return []

    similarities = []

    for faculty in embeddings:

        if faculty["name"] == faculty_name:
            continue

        similarity = cosine_similarity(
            target_embedding,
            faculty["embedding"],
        )

        similarities.append(
            {
                "faculty_id":
                    faculty["faculty_id"],

                "name":
                    faculty["name"],

                "department":
                    faculty["department"],

                "similarity":
                    round(
                        similarity,
                        4,
                    ),
            }
        )

    similarities.sort(
        key=lambda x: x["similarity"],
        reverse=True,
    )

    return similarities[:top_k]


# ======================================================================
# COLLABORATION DISCOVERY
# ======================================================================

def find_complementary_faculty(
    profiles,
    embeddings,
    faculty_name,
    evidence_by_faculty_id,
    graph,
    funding_calls,
    mous=None,
    collaborations=None,
    top_k=5,
    similarity_floor=0.45,
):
    """
    Find evidence-backed collaboration opportunities.

    Pipeline:

        1. Find faculty
        2. Generate semantic similarity
        3. Remove existing collaborators
        4. Check evidence
        5. Calculate complementarity
        6. Check network
        7. Check funding
        8. Check MoU
        9. Calculate final opportunity score
       10. Generate explanation

    Existing collaborators are excluded because this function
    is intended to discover NEW collaboration opportunities.
    """

    target = next(
        (
            faculty
            for faculty in profiles
            if faculty["name"]
            == faculty_name
        ),
        None,
    )

    if target is None:
        return []

    target_embedding = _lookup_embedding(
        embeddings,
        faculty_name,
    )

    if target_embedding is None:
        return []

    target_evidence = (
        evidence_by_faculty_id.get(
            target["faculty_id"]
        )
    )

    if target_evidence is None:
        return []

    existing_pairs = set()

    if collaborations:

        existing_pairs = (
            get_existing_collaboration_pairs(
                collaborations
            )
        )

    opportunities = []

    for candidate in profiles:

        if candidate["name"] == faculty_name:
            continue

        # ----------------------------------------------------------
        # Existing collaboration filter
        # ----------------------------------------------------------

        pair = normalize_pair(
            target["faculty_id"],
            candidate["faculty_id"],
        )

        if pair in existing_pairs:

            continue

        # ----------------------------------------------------------
        # Embedding candidate discovery
        # ----------------------------------------------------------

        candidate_embedding = (
            _lookup_embedding(
                embeddings,
                candidate["name"],
            )
        )

        if candidate_embedding is None:
            continue

        semantic_similarity = (
            cosine_similarity(
                target_embedding,
                candidate_embedding,
            )
        )

        # Embeddings only remove clearly unrelated candidates.
        if (
            semantic_similarity
            < similarity_floor
        ):
            continue

        # ----------------------------------------------------------
        # Evidence
        # ----------------------------------------------------------

        candidate_evidence = (
            evidence_by_faculty_id.get(
                candidate["faculty_id"]
            )
        )

        if candidate_evidence is None:
            continue

        # ----------------------------------------------------------
        # Complementarity
        # ----------------------------------------------------------

        complementarity = (
            calculate_complementarity(
                target_evidence[
                    "combined_keywords"
                ],
                candidate_evidence[
                    "combined_keywords"
                ],
                semantic_similarity,
            )
        )

        # ----------------------------------------------------------
        # Generate full opportunity
        # ----------------------------------------------------------

        opportunity = (
            generate_collaboration_hypothesis(
                faculty_a=target,
                faculty_b=candidate,
                evidence_a=target_evidence,
                evidence_b=candidate_evidence,
                semantic_similarity=
                    semantic_similarity,
                complementarity=
                    complementarity,
                graph=graph,
                funding_calls=funding_calls,
                mous=mous,
            )
        )

        opportunities.append(
            opportunity
        )

    # --------------------------------------------------------------
    # IMPORTANT:
    # Rank by the OVERALL collaboration opportunity score,
    # not simply complementarity.
    # --------------------------------------------------------------

    opportunities.sort(
        key=lambda x:
            x["collaboration_score"],
        reverse=True,
    )

    return opportunities[:top_k]


# ======================================================================
# ALL FACULTY
# ======================================================================

def find_all_candidates(
    profiles,
    embeddings,
    evidence_by_faculty_id,
    graph,
    funding_calls,
    mous=None,
    collaborations=None,
    top_k=5,
):
    """
    Find collaboration opportunities for every faculty member.

    These are recommendations for human review.

    The system does NOT automatically contact researchers,
    submit proposals, or create collaborations.
    """

    candidates = {}

    for faculty in embeddings:

        name = faculty["name"]

        similar = find_similar_faculty(
            embeddings,
            name,
            top_k,
        )

        complementary = (
            find_complementary_faculty(
                profiles=profiles,
                embeddings=embeddings,
                faculty_name=name,
                evidence_by_faculty_id=
                    evidence_by_faculty_id,
                graph=graph,
                funding_calls=funding_calls,
                mous=mous,
                collaborations=
                    collaborations,
                top_k=top_k,
            )
        )

        candidates[name] = {
            "similar": similar,
            "complementary":
                complementary,
        }

    return candidates