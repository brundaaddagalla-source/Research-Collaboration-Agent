from collections import Counter

from sqlalchemy import func

from database.connection import SessionLocal
from models.models import (
    Faculty,
    Collaboration,
    ExternalResearcher,
    FundingCall,
    MoU,
    TrackingRecord,
)


def get_faculty():
    db = SessionLocal()

    try:
        faculty = db.query(Faculty).order_by(Faculty.id).all()

        return [
            {
                "id": item.id,
                "name": item.name,
                "department": item.department,
                "designation": item.designation,
                "research_areas": item.research_areas or [],
                "publications_count": item.publications_count or 0,
                "collaboration_count": item.collaboration_count or 0,
            }
            for item in faculty
        ]

    finally:
        db.close()


def get_expertise_map():
    db = SessionLocal()

    try:
        faculty = db.query(Faculty).all()

        expertise_count = Counter()

        for item in faculty:
            for area in item.research_areas or []:
                expertise_count[area] += 1

        return [
            {
                "research_area": area,
                "faculty_count": count,
            }
            for area, count in expertise_count.most_common()
        ]

    finally:
        db.close()


def get_collaborations():
    db = SessionLocal()

    try:
        collaborations = (
            db.query(Collaboration)
            .order_by(Collaboration.id)
            .all()
        )

        return [
            {
                "id": item.id,
                "faculty_a": item.faculty_a,
                "faculty_b": item.faculty_b,
                "department": item.department,
                "research_areas": item.research_areas or [],
                "collaboration_type": item.collaboration_type,
                "collaboration_strength": item.collaboration_strength,
            }
            for item in collaborations
        ]

    finally:
        db.close()


def get_collaboration_network():
    db = SessionLocal()

    try:
        faculty = db.query(Faculty).order_by(Faculty.id).all()
        collaborations = db.query(Collaboration).all()

        nodes = []

        for item in faculty:
            nodes.append(
                {
                    "id": str(item.id),
                    "label": item.name,
                    "department": item.department,
                }
            )

        faculty_ids = {
            item.name: str(item.id)
            for item in faculty
        }

        edges = []

        for item in collaborations:
            source = faculty_ids.get(item.faculty_a)
            target = faculty_ids.get(item.faculty_b)

            if source and target:
                edges.append(
                    {
                        "source": source,
                        "target": target,
                        "strength": item.collaboration_strength,
                    }
                )

        return {
            "nodes": nodes,
            "edges": edges,
        }

    finally:
        db.close()


def get_opportunities():
    # Agent 24 recommendation logic will generate these later.
    # We should not return fake recommendations.
    return []


def get_external_researchers():
    db = SessionLocal()

    try:
        researchers = (
            db.query(ExternalResearcher)
            .order_by(ExternalResearcher.overall_score.desc())
            .all()
        )

        return [
            {
                "id": item.id,
                "name": item.name,
                "institution": item.institution,
                "country": item.country,
                "research_area": item.research_area,
                "research_fit": item.research_fit,
                "network_reachability": item.network_reachability,
                "overall_score": item.overall_score,
            }
            for item in researchers
        ]

    finally:
        db.close()


def get_funding_opportunities():
    db = SessionLocal()

    try:
        funding = (
            db.query(FundingCall)
            .order_by(FundingCall.deadline)
            .all()
        )

        return [
            {
                "id": item.id,
                "title": item.name,
                "organization": item.organization,
                "deadline": item.deadline.isoformat() if item.deadline else None,
                "research_areas": item.fields or [],
                "consortium_requirement": item.consortium_requirement,
                "international_partner_required": item.international_partner_required,
                "industry_partner_required": item.industry_partner_required,
                "matching_faculty": item.matching_faculty or [],
            }
            for item in funding
        ]

    finally:
        db.close()


def get_mous():
    db = SessionLocal()

    try:
        mous = (
            db.query(MoU)
            .order_by(MoU.id)
            .all()
        )

        return [
            {
                "id": item.id,
                "institution": item.institution,
                "country": item.country,
                "research_area": item.research_area,
                "signed_date": (
                    item.signed_date.isoformat()
                    if item.signed_date
                    else None
                ),
                "last_activity": (
                    item.last_activity.isoformat()
                    if item.last_activity
                    else None
                ),
                "joint_publications": item.joint_publications or 0,
                "joint_projects": item.joint_projects or 0,
                "status": item.status,
            }
            for item in mous
        ]

    finally:
        db.close()


def get_tracking_records():
    db = SessionLocal()

    try:
        records = (
            db.query(TrackingRecord)
            .order_by(TrackingRecord.id)
            .all()
        )

        return [
            {
                "id": item.id,
                "faculty_a": item.faculty_a,
                "faculty_b": item.faculty_b,
                "topic": item.topic,
                "current_stage": item.current_stage,
                "history": item.history or [],
                "last_updated": (
                    item.last_updated.isoformat()
                    if item.last_updated
                    else None
                ),
            }
            for item in records
        ]

    finally:
        db.close()


def get_tracking_stages():
    return [
        "Recommendation",
        "Introduction",
        "Meeting",
        "Proposal",
        "Funded Project",
        "Publication",
    ]


def get_dashboard_summary():
    db = SessionLocal()

    try:
        faculty_count = db.query(Faculty).count()
        collaboration_count = db.query(Collaboration).count()
        external_count = db.query(ExternalResearcher).count()
        funding_count = db.query(FundingCall).count()

        research_areas = set()

        faculty = db.query(Faculty).all()

        for item in faculty:
            for area in item.research_areas or []:
                research_areas.add(area)

        dormant_mous = (
            db.query(MoU)
            .filter(
                func.lower(MoU.status) == "dormant"
            )
            .count()
        )

        return {
            "faculty_count": faculty_count,
            "research_areas": len(research_areas),
            "existing_collaborations": collaboration_count,
            "potential_collaborations": 0,
            "external_candidates": external_count,
            "funding_matches": funding_count,
            "dormant_mous": dormant_mous,
        }

    finally:
        db.close()


def get_collaboration_activity():
    # There is currently no collaboration-date field in the
    # prototype Collaboration model, so we should not fabricate
    # monthly activity.
    return []