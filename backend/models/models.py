from datetime import date, datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Date,
    DateTime,
    JSON,
    ForeignKey,
)
from database.connection import Base


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    department = Column(String(200), nullable=False)
    designation = Column(String(100))
    research_areas = Column(JSON)
    publications_count = Column(Integer, default=0)
    collaboration_count = Column(Integer, default=0)

    # Agent 24 v2: faculty email, used for the collaboration-request
    # notification workflow (see services/email_service.py). Added via
    # migration on existing databases - see database/migrate_agent24_v2.py,
    # which adds the column, backfills the known 8 faculty emails, then
    # applies this NOT NULL constraint at the database level.
    email = Column(String(255), unique=True, nullable=False)


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    faculty_name = Column(String(200), nullable=False)
    year = Column(Integer)
    venue = Column(String(300))
    doi = Column(String(200))


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    faculty_name = Column(String(200), nullable=False)
    description = Column(Text)
    research_area = Column(String(200))
    status = Column(String(100))


class Collaboration(Base):
    __tablename__ = "collaborations"

    id = Column(Integer, primary_key=True, index=True)
    faculty_a = Column(String(200), nullable=False)
    faculty_b = Column(String(200), nullable=False)
    department = Column(String(200))
    research_areas = Column(JSON)
    collaboration_type = Column(String(200))
    collaboration_strength = Column(String(50))


class ExternalResearcher(Base):
    __tablename__ = "external_researchers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    institution = Column(String(300))
    country = Column(String(100))

    research_interests = Column(JSON)
    skills = Column(JSON)

    # Keep these for Agent 24 scoring
    research_area = Column(String(200))
    research_fit = Column(Integer)
    network_reachability = Column(String(50))
    overall_score = Column(Integer)


class FundingCall(Base):
    __tablename__ = "funding_calls"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(500), nullable=False)
    organization = Column(String(300))
    amount = Column(Integer)
    deadline = Column(Date)

    fields = Column(JSON)
    eligibility = Column(JSON)
    research_stage = Column(JSON)
    keywords = Column(JSON)

    consortium_requirement = Column(Boolean, default=False)
    international_partner_required = Column(Boolean, default=False)
    industry_partner_required = Column(Boolean, default=False)

    matching_faculty = Column(JSON)


class MoU(Base):
    __tablename__ = "mous"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(300), nullable=False)
    country = Column(String(100))
    research_area = Column(String(200))

    signed_date = Column(Date)
    last_activity = Column(Date)

    joint_publications = Column(Integer, default=0)
    joint_projects = Column(Integer, default=0)

    status = Column(String(100))


class TrackingRecord(Base):
    __tablename__ = "tracking_records"

    id = Column(Integer, primary_key=True, index=True)

    faculty_a = Column(String(200), nullable=False)
    faculty_b = Column(String(200))

    external_researcher_id = Column(Integer)
    external_institution = Column(String(300))

    topic = Column(String(500))
    current_stage = Column(String(100))
    history = Column(JSON)
    last_updated = Column(Date)


class FacultyCredential(Base):
    """
    Login credentials for the Faculty Login page (JWT auth).

    grid_secret contains 16 grid values:

    {
        "G1": "...",
        "G2": "...",
        ...
        "G16": "..."
    }

    Every faculty member has the same grid positions, but each
    position can have its own secret value.
    """
    __tablename__ = "faculty_credentials"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    password_hash = Column(String(255), nullable=False)
    grid_secret = Column(JSON, nullable=False)


# ============================================================
# AGENT 24 v2 - FACULTY COLLABORATION SYSTEM
# ============================================================
#
# Everything below is additive: new tables only. Nothing above this
# line is modified except Faculty.email (see above). These tables are
# intentionally NOT touched by seed.py's delete-and-reseed cycle -
# they hold real, faculty-generated data (uploaded documents,
# collaboration requests, email response tokens) that must survive a
# re-run of the mock-data seed script.


class FacultyResearchDocument(Base):
    """
    A piece of existing research work a faculty member has uploaded to
    their profile (PDF/DOC/DOCX). Used as extra matching evidence by
    the collaboration search (services/matching_service.py).
    """
    __tablename__ = "faculty_research_documents"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False, index=True)

    title = Column(String(500), nullable=False)
    keywords = Column(JSON, default=list)

    file_name = Column(String(255), nullable=False)  # original filename, for display only
    file_type = Column(String(10), nullable=False)  # pdf | doc | docx
    file_reference = Column(String(500), nullable=False)  # storage path/reference, never the raw bytes

    extracted_text = Column(Text, nullable=True)
    extraction_status = Column(String(50), default="pending")  # extracted | unavailable | pending

    uploaded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CollaborationRequest(Base):
    """
    One faculty-to-faculty collaboration request, moving through the
    faculty-approval -> authority-approval lifecycle described in the
    Agent 24 v2 spec (routes/collaboration_requests.py).
    """
    __tablename__ = "collaboration_requests"

    id = Column(Integer, primary_key=True, index=True)

    requester_faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False, index=True)
    target_faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False, index=True)
    target_external_researcher_id = Column(Integer,ForeignKey("external_researchers.id"),nullable=True,index=True,)
    topic = Column(String(500), nullable=False)
    proposal = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)

    matching_score = Column(Integer, nullable=True)
    matching_evidence = Column(JSON, nullable=True)  # {matching_expertise, relevant_publications, ...}

    funding_id = Column(Integer, ForeignKey("funding_calls.id"), nullable=True)
    mou_id = Column(Integer, ForeignKey("mous.id"), nullable=True)

    university_benefit = Column(Text, nullable=True)

    # PENDING | APPROVED | REJECTED
    faculty_status = Column(String(50), default="PENDING", nullable=False)
    faculty_comments = Column(Text, nullable=True)
    faculty_responded_at = Column(DateTime, nullable=True)

    # PENDING | APPROVED | REJECTED | MORE_INFORMATION
    authority_status = Column(String(50), default="PENDING", nullable=False)
    authority_comments = Column(Text, nullable=True)
    authority_responded_at = Column(DateTime, nullable=True)

    # REQUESTED | FACULTY_REJECTED | ACCEPTED | AUTHORITY_REJECTED | ACTIVE
    # ACCEPTED = the target faculty has accepted the invitation and it is
    # now pending the authority's final approval (formerly labeled
    # AUTHORITY_REVIEW - renamed so the faculty-facing status reads
    # "Accepted" immediately after their own acceptance, per spec).
    stage = Column(String(50), default="REQUESTED", nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CollaborationResponseToken(Base):
    __tablename__ = "collaboration_response_tokens"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(
        Integer,
        ForeignKey("collaboration_requests.id"),
        nullable=False,
        index=True,
    )

    recipient_faculty_id = Column(
        Integer,
        ForeignKey("faculty.id"),
        nullable=True,
    )

    recipient_external_researcher_id = Column(
        Integer,
        ForeignKey("external_researchers.id"),
        nullable=True,
        index=True,
    )

    action = Column(String(50), nullable=False)

    token_hash = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    expires_at = Column(DateTime, nullable=False)

    used_at = Column(DateTime, nullable=True)