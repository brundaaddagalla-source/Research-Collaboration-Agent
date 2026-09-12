from datetime import date

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, JSON
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