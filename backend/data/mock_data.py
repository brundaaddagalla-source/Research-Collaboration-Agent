"""
Mock / in-memory data for Agent 24 - Research Collaboration Agent (Phase 1).

IMPORTANT: None of this data is computed or inferred by any algorithm.
It is hand-written mock data used only to build and test the frontend <-> backend
connection. Real logic (expertise mapping, network analysis, scoring, etc.)
will replace this in Phase 2+.
"""

# ---------------------------------------------------------------------------
# DASHBOARD SUMMARY
# ---------------------------------------------------------------------------

DASHBOARD_SUMMARY = {
    "faculty_count": 124,
    "research_areas": 38,
    "existing_collaborations": 86,
    "potential_collaborations": 24,
    "external_candidates": 41,
    "funding_matches": 12,
    "dormant_mous": 5,
}

# Simple mock time-series for a "collaboration activity" chart on the dashboard
COLLABORATION_ACTIVITY = [
    {"month": "Apr", "new_collaborations": 3, "introductions": 5},
    {"month": "May", "new_collaborations": 5, "introductions": 7},
    {"month": "Jun", "new_collaborations": 4, "introductions": 6},
    {"month": "Jul", "new_collaborations": 7, "introductions": 9},
    {"month": "Aug", "new_collaborations": 6, "introductions": 8},
    {"month": "Sep", "new_collaborations": 9, "introductions": 11},
]

# ---------------------------------------------------------------------------
# FACULTY
# ---------------------------------------------------------------------------

FACULTY = [
    {
        "id": 1,
        "name": "Dr. Ananya Rao",
        "department": "Computer Science & Engineering",
        "designation": "Associate Professor",
        "research_areas": ["Computer Vision", "Deep Learning"],
        "publications_count": 42,
        "collaboration_count": 6,
    },
    {
        "id": 2,
        "name": "Dr. Rahul Sharma",
        "department": "Civil Engineering",
        "designation": "Professor",
        "research_areas": ["Hydrology", "Climate Science"],
        "publications_count": 58,
        "collaboration_count": 4,
    },
    {
        "id": 3,
        "name": "Dr. Priya Menon",
        "department": "Electronics & Communication Engineering",
        "designation": "Assistant Professor",
        "research_areas": ["Remote Sensing", "Signal Processing"],
        "publications_count": 27,
        "collaboration_count": 3,
    },
    {
        "id": 4,
        "name": "Dr. Vikram Nair",
        "department": "Computer Science & Engineering",
        "designation": "Professor",
        "research_areas": ["Artificial Intelligence", "Natural Language Processing"],
        "publications_count": 71,
        "collaboration_count": 9,
    },
    {
        "id": 5,
        "name": "Dr. Kavitha Reddy",
        "department": "Biotechnology",
        "designation": "Associate Professor",
        "research_areas": ["Genomics", "Bioinformatics"],
        "publications_count": 35,
        "collaboration_count": 5,
    },
    {
        "id": 6,
        "name": "Dr. Suresh Iyer",
        "department": "Mechanical Engineering",
        "designation": "Professor",
        "research_areas": ["Renewable Energy", "Thermal Systems"],
        "publications_count": 49,
        "collaboration_count": 7,
    },
    {
        "id": 7,
        "name": "Dr. Meera Krishnan",
        "department": "Civil Engineering",
        "designation": "Assistant Professor",
        "research_areas": ["Climate Science", "Disaster Risk Management"],
        "publications_count": 19,
        "collaboration_count": 2,
    },
    {
        "id": 8,
        "name": "Dr. Arjun Desai",
        "department": "Computer Science & Engineering",
        "designation": "Assistant Professor",
        "research_areas": ["Robotics", "Computer Vision"],
        "publications_count": 22,
        "collaboration_count": 3,
    },
]

# ---------------------------------------------------------------------------
# EXPERTISE MAP
# ---------------------------------------------------------------------------

EXPERTISE_MAP = [
    {"research_area": "Computer Vision", "faculty_count": 12},
    {"research_area": "Artificial Intelligence", "faculty_count": 18},
    {"research_area": "Remote Sensing", "faculty_count": 7},
    {"research_area": "Climate Science", "faculty_count": 5},
    {"research_area": "Hydrology", "faculty_count": 4},
    {"research_area": "Bioinformatics", "faculty_count": 9},
    {"research_area": "Renewable Energy", "faculty_count": 11},
    {"research_area": "Robotics", "faculty_count": 8},
    {"research_area": "Natural Language Processing", "faculty_count": 10},
    {"research_area": "Disaster Risk Management", "faculty_count": 3},
]

# ---------------------------------------------------------------------------
# EXISTING COLLABORATIONS (for the network page)
# ---------------------------------------------------------------------------

COLLABORATIONS = [
    {
        "id": 1,
        "faculty_a": "Dr. Ananya Rao",
        "faculty_b": "Dr. Arjun Desai",
        "department": "Computer Science & Engineering",
        "research_areas": ["Computer Vision"],
        "collaboration_type": "Co-authored publication",
        "collaboration_strength": "Strong",
    },
    {
        "id": 2,
        "faculty_a": "Dr. Rahul Sharma",
        "faculty_b": "Dr. Meera Krishnan",
        "department": "Civil Engineering",
        "research_areas": ["Climate Science", "Hydrology"],
        "collaboration_type": "Joint research project",
        "collaboration_strength": "Moderate",
    },
    {
        "id": 3,
        "faculty_a": "Dr. Vikram Nair",
        "faculty_b": "Dr. Priya Menon",
        "department": "Cross-department",
        "research_areas": ["Artificial Intelligence", "Signal Processing"],
        "collaboration_type": "Co-authored publication",
        "collaboration_strength": "Moderate",
    },
    {
        "id": 4,
        "faculty_a": "Dr. Kavitha Reddy",
        "faculty_b": "Dr. Suresh Iyer",
        "department": "Cross-department",
        "research_areas": ["Bioinformatics", "Renewable Energy"],
        "collaboration_type": "Joint grant",
        "collaboration_strength": "Weak",
    },
]

# Mock node/edge structure for the collaboration network placeholder page
COLLABORATION_NETWORK = {
    "nodes": [
        {"id": "ananya_rao", "label": "Dr. Ananya Rao", "department": "CSE"},
        {"id": "arjun_desai", "label": "Dr. Arjun Desai", "department": "CSE"},
        {"id": "rahul_sharma", "label": "Dr. Rahul Sharma", "department": "Civil"},
        {"id": "meera_krishnan", "label": "Dr. Meera Krishnan", "department": "Civil"},
        {"id": "vikram_nair", "label": "Dr. Vikram Nair", "department": "CSE"},
        {"id": "priya_menon", "label": "Dr. Priya Menon", "department": "ECE"},
        {"id": "kavitha_reddy", "label": "Dr. Kavitha Reddy", "department": "Biotech"},
        {"id": "suresh_iyer", "label": "Dr. Suresh Iyer", "department": "Mechanical"},
    ],
    "edges": [
        {"source": "ananya_rao", "target": "arjun_desai", "strength": "Strong"},
        {"source": "rahul_sharma", "target": "meera_krishnan", "strength": "Moderate"},
        {"source": "vikram_nair", "target": "priya_menon", "strength": "Moderate"},
        {"source": "kavitha_reddy", "target": "suresh_iyer", "strength": "Weak"},
    ],
}

# ---------------------------------------------------------------------------
# INTERNAL OPPORTUNITIES (potential collaborations)
# ---------------------------------------------------------------------------

OPPORTUNITIES = [
    {
        "id": 1,
        "faculty_a": "Dr. Ananya Rao",
        "faculty_b": "Dr. Rahul Sharma",
        "department_a": "Computer Science & Engineering",
        "department_b": "Civil Engineering",
        "research_areas": ["Computer Vision", "Hydrology"],
        "compatibility_score": 91,
        "complementarity_score": 88,
        "reason": (
            "Their research areas are complementary and neither faculty member "
            "has previously collaborated with the other. Potential focus: "
            "AI-based GLOF (Glacial Lake Outburst Flood) monitoring and early warning."
        ),
        "status": "Suggested",
    },
    {
        "id": 2,
        "faculty_a": "Dr. Priya Menon",
        "faculty_b": "Dr. Meera Krishnan",
        "department_a": "Electronics & Communication Engineering",
        "department_b": "Civil Engineering",
        "research_areas": ["Remote Sensing", "Disaster Risk Management"],
        "compatibility_score": 84,
        "complementarity_score": 79,
        "reason": (
            "Remote sensing expertise could support satellite-based disaster "
            "risk mapping, an area currently unexplored by either faculty member."
        ),
        "status": "Suggested",
    },
    {
        "id": 3,
        "faculty_a": "Dr. Vikram Nair",
        "faculty_b": "Dr. Kavitha Reddy",
        "department_a": "Computer Science & Engineering",
        "department_b": "Biotechnology",
        "research_areas": ["Artificial Intelligence", "Genomics"],
        "compatibility_score": 77,
        "complementarity_score": 82,
        "reason": (
            "AI-driven genomic sequence analysis is an emerging cross-disciplinary "
            "area that neither department has actively pursued together."
        ),
        "status": "Under Review",
    },
    {
        "id": 4,
        "faculty_a": "Dr. Suresh Iyer",
        "faculty_b": "Dr. Arjun Desai",
        "department_a": "Mechanical Engineering",
        "department_b": "Computer Science & Engineering",
        "research_areas": ["Renewable Energy", "Robotics"],
        "compatibility_score": 73,
        "complementarity_score": 70,
        "reason": (
            "Robotics-assisted maintenance for renewable energy installations "
            "is a growing niche with no current internal collaboration."
        ),
        "status": "Suggested",
    },
]

# ---------------------------------------------------------------------------
# EXTERNAL RESEARCHERS
# ---------------------------------------------------------------------------

EXTERNAL_RESEARCHERS = [
    {
        "id": 1,
        "name": "Dr. Sarah Thompson",
        "institution": "University of Melbourne",
        "country": "Australia",
        "research_area": "Climate Modeling",
        "research_fit": 88,
        "network_reachability": "Medium",
        "overall_score": 85,
    },
    {
        "id": 2,
        "name": "Dr. Kenji Watanabe",
        "institution": "Tokyo Institute of Technology",
        "country": "Japan",
        "research_area": "Computer Vision",
        "research_fit": 92,
        "network_reachability": "High",
        "overall_score": 90,
    },
    {
        "id": 3,
        "name": "Dr. Lena Fischer",
        "institution": "ETH Zurich",
        "country": "Switzerland",
        "research_area": "Hydrology",
        "research_fit": 81,
        "network_reachability": "Low",
        "overall_score": 74,
    },
    {
        "id": 4,
        "name": "Dr. Michael Obi",
        "institution": "University of Cape Town",
        "country": "South Africa",
        "research_area": "Renewable Energy",
        "research_fit": 79,
        "network_reachability": "Medium",
        "overall_score": 76,
    },
    {
        "id": 5,
        "name": "Dr. Wei Zhang",
        "institution": "National University of Singapore",
        "country": "Singapore",
        "research_area": "Bioinformatics",
        "research_fit": 86,
        "network_reachability": "High",
        "overall_score": 87,
    },
]

# ---------------------------------------------------------------------------
# FUNDING & CONSORTIUMS
# ---------------------------------------------------------------------------

FUNDING_OPPORTUNITIES = [
    {
        "id": 1,
        "title": "Indo-Australian Joint Research Grant on Climate Resilience",
        "organization": "Department of Science & Technology (DST)",
        "deadline": "2026-11-15",
        "research_areas": ["Climate Science", "Hydrology"],
        "consortium_requirement": True,
        "international_partner_required": True,
        "industry_partner_required": False,
        "matching_faculty": ["Dr. Rahul Sharma", "Dr. Meera Krishnan"],
    },
    {
        "id": 2,
        "title": "AI for Earth Observation Challenge",
        "organization": "Department of Biotechnology (DBT)",
        "deadline": "2026-10-30",
        "research_areas": ["Computer Vision", "Remote Sensing"],
        "consortium_requirement": False,
        "international_partner_required": False,
        "industry_partner_required": True,
        "matching_faculty": ["Dr. Ananya Rao", "Dr. Priya Menon"],
    },
    {
        "id": 3,
        "title": "Renewable Energy Innovation Fund",
        "organization": "Ministry of New and Renewable Energy (MNRE)",
        "deadline": "2026-12-05",
        "research_areas": ["Renewable Energy"],
        "consortium_requirement": True,
        "international_partner_required": False,
        "industry_partner_required": True,
        "matching_faculty": ["Dr. Suresh Iyer"],
    },
    {
        "id": 4,
        "title": "Genomics for Public Health Consortium",
        "organization": "Indian Council of Medical Research (ICMR)",
        "deadline": "2027-01-20",
        "research_areas": ["Genomics", "Bioinformatics"],
        "consortium_requirement": True,
        "international_partner_required": True,
        "industry_partner_required": False,
        "matching_faculty": ["Dr. Kavitha Reddy"],
    },
]

# ---------------------------------------------------------------------------
# MoU INTELLIGENCE
# ---------------------------------------------------------------------------

MOUS = [
    {
        "id": 1,
        "institution": "Tokyo Institute of Technology",
        "country": "Japan",
        "research_area": "Computer Vision",
        "signed_date": "2022-03-10",
        "last_activity": "2026-06-02",
        "joint_publications": 6,
        "joint_projects": 2,
        "status": "Active",
    },
    {
        "id": 2,
        "institution": "ETH Zurich",
        "country": "Switzerland",
        "research_area": "Hydrology",
        "signed_date": "2021-08-22",
        "last_activity": "2024-11-14",
        "joint_publications": 1,
        "joint_projects": 0,
        "status": "Underutilized",
    },
    {
        "id": 3,
        "institution": "University of Cape Town",
        "country": "South Africa",
        "research_area": "Renewable Energy",
        "signed_date": "2019-05-18",
        "last_activity": "2020-09-30",
        "joint_publications": 0,
        "joint_projects": 0,
        "status": "Dormant",
    },
    {
        "id": 4,
        "institution": "National University of Singapore",
        "country": "Singapore",
        "research_area": "Bioinformatics",
        "signed_date": "2023-01-05",
        "last_activity": "2026-08-19",
        "joint_publications": 4,
        "joint_projects": 3,
        "status": "Active",
    },
    {
        "id": 5,
        "institution": "University of Melbourne",
        "country": "Australia",
        "research_area": "Climate Science",
        "signed_date": "2020-02-12",
        "last_activity": "2022-04-07",
        "joint_publications": 2,
        "joint_projects": 0,
        "status": "Dormant",
    },
]

# ---------------------------------------------------------------------------
# COLLABORATION TRACKING PIPELINE
# ---------------------------------------------------------------------------

TRACKING_STAGES = ["Recommendation", "Introduction", "Meeting", "Proposal", "Funded Project", "Publication"]

TRACKING_RECORDS = [
    {
        "id": 1,
        "faculty_a": "Dr. Ananya Rao",
        "faculty_b": "Dr. Rahul Sharma",
        "topic": "AI-based GLOF monitoring and early warning",
        "current_stage": "Meeting",
        "history": ["Recommendation", "Introduction", "Meeting"],
        "last_updated": "2026-09-02",
    },
    {
        "id": 2,
        "faculty_a": "Dr. Vikram Nair",
        "faculty_b": "Dr. Kavitha Reddy",
        "topic": "AI-driven genomic sequence analysis",
        "current_stage": "Introduction",
        "history": ["Recommendation", "Introduction"],
        "last_updated": "2026-08-21",
    },
    {
        "id": 3,
        "faculty_a": "Dr. Priya Menon",
        "faculty_b": "Dr. Meera Krishnan",
        "topic": "Satellite-based disaster risk mapping",
        "current_stage": "Proposal",
        "history": ["Recommendation", "Introduction", "Meeting", "Proposal"],
        "last_updated": "2026-08-30",
    },
    {
        "id": 4,
        "faculty_a": "Dr. Suresh Iyer",
        "faculty_b": "Dr. Arjun Desai",
        "topic": "Robotics-assisted renewable energy maintenance",
        "current_stage": "Recommendation",
        "history": ["Recommendation"],
        "last_updated": "2026-09-08",
    },
    {
        "id": 5,
        "faculty_a": "Dr. Kavitha Reddy",
        "faculty_b": "Dr. Wei Zhang",
        "topic": "Cross-border bioinformatics pipeline development",
        "current_stage": "Funded Project",
        "history": ["Recommendation", "Introduction", "Meeting", "Proposal", "Funded Project"],
        "last_updated": "2026-07-15",
    },
]
