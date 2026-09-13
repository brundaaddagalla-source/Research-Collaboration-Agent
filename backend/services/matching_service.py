"""
Collaboration matching (spec sections 10-12, 51).

Deliberately simple and explainable, per spec section 51 ("Do not
introduce expensive LLM APIs... complicated vector databases...").
The score is a deterministic sum of keyword/expertise overlap across:

  - Faculty.research_areas
  - Publication titles
  - Project titles/descriptions/research_area
  - FacultyResearchDocument title/keywords/extracted_text

Existing collaboration history is surfaced as context only and never
used to penalize a candidate (spec section 12) - Agent 24's purpose
here is discovering NEW collaborations.

Structured so a smarter matching engine (embeddings, an LLM re-ranker,
etc.) can be swapped in later behind the same `search_collaborators`
function signature.
"""

import re
from collections import defaultdict

from sqlalchemy.orm import Session

from models.models import (
    Faculty,
    Publication,
    Project,
    Collaboration,
    FacultyResearchDocument,
    FundingCall,
    MoU,
)

STOPWORDS = {
    "a", "an", "the", "for", "of", "and", "or", "in", "on", "to", "with",
    "using", "via", "based", "into", "at", "by", "as", "is", "are",
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
    return [w for w in words if len(w) >= 3 and w not in STOPWORDS]


def _text_matches(text: str, tokens: list[str]) -> bool:
    if not text or not tokens:
        return False
    lowered = text.lower()
    return any(token in lowered for token in tokens)


def _score_one_faculty(query_tokens, faculty, publications, projects, documents):
    matching_expertise = []
    for area in faculty.research_areas or []:
        if _text_matches(area, query_tokens):
            matching_expertise.append(area)

    relevant_publications = [p.title for p in publications if _text_matches(p.title, query_tokens)]

    relevant_projects = [
        p.title
        for p in projects
        if _text_matches(f"{p.title} {p.description or ''} {p.research_area or ''}", query_tokens)
    ]

    relevant_research_work = [
        d.title
        for d in documents
        if _text_matches(
            f"{d.title} {' '.join(d.keywords or [])} {d.extracted_text or ''}",
            query_tokens,
        )
    ]

    score = 0
    score += min(len(matching_expertise) * 25, 50)
    score += min(len(relevant_publications) * 10, 20)
    score += min(len(relevant_projects) * 10, 20)
    score += min(len(relevant_research_work) * 10, 20)
    score = min(score, 100)

    return score, matching_expertise, relevant_publications, relevant_projects, relevant_research_work


def _build_reason(faculty_name, matching_expertise, relevant_publications, relevant_projects, relevant_research_work):
    parts = []
    if matching_expertise:
        parts.append(f"overlapping expertise in {', '.join(matching_expertise)}")
    if relevant_publications:
        parts.append(f"{len(relevant_publications)} relevant publication(s)")
    if relevant_projects:
        parts.append(f"{len(relevant_projects)} relevant project(s)")
    if relevant_research_work:
        parts.append(f"{len(relevant_research_work)} relevant uploaded research document(s)")

    if not parts:
        return f"{faculty_name} does not yet have strong evidence on file for this topic."

    return f"{faculty_name} shows " + "; ".join(parts) + "."


def _relevant_funding(query_tokens, matching_expertise, funding_calls):
    tokens = set(query_tokens) | {e.lower() for e in matching_expertise}
    matches = []
    for call in funding_calls:
        haystack = " ".join((call.fields or []) + (call.keywords or []) + [call.name or ""])
        if _text_matches(haystack, list(tokens)):
            matches.append({"id": call.id, "name": call.name, "organization": call.organization})
    return matches


def _relevant_mou(query_tokens, matching_expertise, mous):
    tokens = set(query_tokens) | {e.lower() for e in matching_expertise}
    matches = []
    for mou in mous:
        haystack = f"{mou.research_area or ''}"
        if _text_matches(haystack, list(tokens)) and (mou.status or "").lower() != "dormant":
            matches.append({"id": mou.id, "institution": mou.institution, "status": mou.status})
    return matches


def score_candidate(db: Session, faculty_id: int, query: str) -> dict | None:
    """
    Score a single, specific faculty member against a query. Used when
    creating a collaboration request, so the stored matching_score /
    matching_evidence is always computed server-side from the same
    deterministic logic as the search results - never trusted from the
    frontend (spec section 14).
    """
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        return None

    query_tokens = tokenize(query)

    publications = db.query(Publication).filter(Publication.faculty_name == faculty.name).all()
    projects = db.query(Project).filter(Project.faculty_name == faculty.name).all()
    documents = (
        db.query(FacultyResearchDocument)
        .filter(FacultyResearchDocument.faculty_id == faculty.id)
        .all()
    )
    funding_calls = db.query(FundingCall).all()
    mous = db.query(MoU).all()

    score, matching_expertise, relevant_publications, relevant_projects, relevant_research_work = (
        _score_one_faculty(query_tokens, faculty, publications, projects, documents)
    )

    return {
        "faculty": {
            "faculty_id": str(faculty.id),
            "name": faculty.name,
            "department": faculty.department,
            "designation": faculty.designation,
        },
        "score": score,
        "matching_expertise": matching_expertise,
        "relevant_publications": relevant_publications,
        "relevant_projects": relevant_projects,
        "relevant_research_work": relevant_research_work,
        "funding_opportunities": _relevant_funding(query_tokens, matching_expertise, funding_calls),
        "mou_opportunities": _relevant_mou(query_tokens, matching_expertise, mous),
        "reason": _build_reason(
            faculty.name, matching_expertise, relevant_publications, relevant_projects, relevant_research_work
        ),
    }


def search_collaborators(db: Session, current_faculty_id: int, query: str, top_k: int = 10) -> list[dict]:
    query_tokens = tokenize(query)

    faculty_list = db.query(Faculty).filter(Faculty.id != current_faculty_id).order_by(Faculty.id).all()
    if not faculty_list:
        return []

    all_publications = db.query(Publication).all()
    all_projects = db.query(Project).all()
    all_documents = db.query(FacultyResearchDocument).all()
    funding_calls = db.query(FundingCall).all()
    mous = db.query(MoU).all()

    pubs_by_name = defaultdict(list)
    for p in all_publications:
        pubs_by_name[p.faculty_name].append(p)

    projects_by_name = defaultdict(list)
    for p in all_projects:
        projects_by_name[p.faculty_name].append(p)

    docs_by_faculty_id = defaultdict(list)
    for d in all_documents:
        docs_by_faculty_id[d.faculty_id].append(d)

    results = []
    for faculty in faculty_list:
        publications = pubs_by_name.get(faculty.name, [])
        projects = projects_by_name.get(faculty.name, [])
        documents = docs_by_faculty_id.get(faculty.id, [])

        score, matching_expertise, relevant_publications, relevant_projects, relevant_research_work = (
            _score_one_faculty(query_tokens, faculty, publications, projects, documents)
        )

        # Evidence-based, not "same keyword = match": every candidate is
        # returned with the *reason* they were or weren't a strong match,
        # rather than being silently dropped. Callers can filter on score.
        results.append(
            {
                "faculty": {
                    "faculty_id": str(faculty.id),
                    "name": faculty.name,
                    "department": faculty.department,
                    "designation": faculty.designation,
                },
                "score": score,
                "matching_expertise": matching_expertise,
                "relevant_publications": relevant_publications,
                "relevant_projects": relevant_projects,
                "relevant_research_work": relevant_research_work,
                "funding_opportunities": _relevant_funding(query_tokens, matching_expertise, funding_calls),
                "mou_opportunities": _relevant_mou(query_tokens, matching_expertise, mous),
                "reason": _build_reason(
                    faculty.name, matching_expertise, relevant_publications, relevant_projects, relevant_research_work
                ),
            }
        )

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]