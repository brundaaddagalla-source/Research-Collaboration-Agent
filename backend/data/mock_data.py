"""
Mock / in-memory data for Agent 24 - Research Collaboration Agent (Phase 1).

IMPORTANT: None of this data is computed or inferred by any algorithm.
It is hand-written mock data used only to build and test the frontend <-> backend
connection. Real logic (expertise mapping, network analysis, scoring, etc.)
will replace this in Phase 2+.
"""



# ---------------------------------------------------------------------------
# FACULTY
# ---------------------------------------------------------------------------

FACULTY = [
    {
        "id": 10243,
        "name": "Dr. Ananya Rao",
        "email": "brunda1705@gmail.com",
        "department": "Computer Science & Engineering",
        "designation": "Associate Professor",
        "research_areas": [
            "Computer Vision",
            "Deep Learning",
        ],
        "publications_count": 42,
        "collaboration_count": 6,
    },
    {
        "id": 22345,
        "name": "Dr. Rahul Sharma",
        "email": "brundaaddagalla@gmail.com",
        "department": "Civil Engineering",
        "designation": "Professor",
        "research_areas": [
            "Hydrology",
            "Climate Science",
        ],
        "publications_count": 58,
        "collaboration_count": 4,
    },
    {
        "id": 31452,
        "name": "Dr. Priya Menon",
        "email": "addagallabrunda@gmail.com",
        "department": "Electronics & Communication Engineering",
        "designation": "Assistant Professor",
        "research_areas": [
            "Remote Sensing",
            "Signal Processing",
        ],
        "publications_count": 27,
        "collaboration_count": 3,
    },
    {
        "id": 42561,
        "name": "Dr. Vikram Nair",
        "email": "vu.241fa4606@gmail.com",
        "department": "Computer Science & Engineering",
        "designation": "Professor",
        "research_areas": [
            "Artificial Intelligence",
            "Natural Language Processing",
        ],
        "publications_count": 71,
        "collaboration_count": 9,
    },
    {
        "id": 53672,
        "name": "Dr. Kavitha Reddy",
        "email": "vu.241fa04610@gmail.com",
        "department": "Biotechnology",
        "designation": "Associate Professor",
        "research_areas": [
            "Genomics",
            "Bioinformatics",
        ],
        "publications_count": 35,
        "collaboration_count": 5,
    },
    {
        "id": 64783,
        "name": "Dr. Suresh Iyer",
        "email": "mandurigiridharkrishna@gmail.com",
        "department": "Mechanical Engineering",
        "designation": "Professor",
        "research_areas": [
            "Renewable Energy",
            "Thermal Systems",
        ],
        "publications_count": 49,
        "collaboration_count": 7,
    },
    {
        "id": 75894,
        "name": "Dr. Meera Krishnan",
        "email": "giridharkrishna1017@gmail.com",
        "department": "Civil Engineering",
        "designation": "Assistant Professor",
        "research_areas": [
            "Climate Science",
            "Disaster Risk Management",
        ],
        "publications_count": 19,
        "collaboration_count": 2,
    },
    {
        "id": 86915,
        "name": "Dr. Arjun Desai",
        "email": "krishnacontact0708@gmail.com",
        "department": "Computer Science & Engineering",
        "designation": "Assistant Professor",
        "research_areas": [
            "Robotics",
            "Computer Vision",
        ],
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
        "email": "brunda1705@gmail.com",
        "institution": "University of Melbourne",
        "country": "Australia",
        "research_interests": [
            "Climate Science",
            "Climate Modeling",
            "Hydrology",
            "Disaster Risk Management",
        ],
        "skills": [
            "Climate Modeling",
            "Data Analysis",
            "Hydrological Simulation",
        ],
        "research_area": "Climate Modeling",
        "research_fit": 88,
        "network_reachability": "Medium",
        "overall_score": 85,
    },

    {
        "id": 2,
        "name": "Dr. Kenji Watanabe",
        "email": "brunda1705@gmail.com",
        "institution": "Tokyo Institute of Technology",
        "country": "Japan",
        "research_interests": [
            "Computer Vision",
            "Artificial Intelligence",
            "Deep Learning",
            "Robotics",
        ],
        "skills": [
            "Python",
            "Deep Learning",
            "Computer Vision",
            "Image Processing",
        ],
        "research_area": "Computer Vision",
        "research_fit": 92,
        "network_reachability": "High",
        "overall_score": 90,
    },

    {
        "id": 3,
        "name": "Dr. Lena Fischer",
        "email": "brunda1705@gmail.com",
        "institution": "ETH Zurich",
        "country": "Switzerland",
        "research_interests": [
            "Hydrology",
            "Climate Science",
            "Flood Modeling",
            "Water Resources",
        ],
        "skills": [
            "Hydrological Modeling",
            "Climate Data Analysis",
            "Flood Prediction",
        ],
        "research_area": "Hydrology",
        "research_fit": 81,
        "network_reachability": "Low",
        "overall_score": 74,
    },

    {
        "id": 4,
        "name": "Dr. Michael Obi",
        "email": "brunda1705@gmail.com",
        "institution": "University of Cape Town",
        "country": "South Africa",
        "research_interests": [
            "Renewable Energy",
            "Energy Systems",
            "Sustainable Engineering",
        ],
        "skills": [
            "Energy Optimization",
            "Solar Energy",
            "Energy Systems Modeling",
        ],
        "research_area": "Renewable Energy",
        "research_fit": 79,
        "network_reachability": "Medium",
        "overall_score": 76,
    },

    {
        "id": 5,
        "name": "Dr. Wei Zhang",
        "email": "brunda1705@gmail.com",
        "institution": "National University of Singapore",
        "country": "Singapore",
        "research_interests": [
            "Bioinformatics",
            "Genomics",
            "Computational Biology",
            "Machine Learning",
        ],
        "skills": [
            "Python",
            "Machine Learning",
            "Genomic Data Analysis",
            "Bioinformatics",
        ],
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
        "name": "Indo-Australian Joint Research Grant on Climate Resilience",
        "organization": "Department of Science & Technology (DST)",
        "amount": 1000000,
        "deadline": "2026-11-15",

        "fields": [
            "Climate Science",
            "Hydrology",
            "Disaster Risk Management",
        ],

        "eligibility": [
            "Faculty",
            "Research Scholars",
        ],

        "research_stage": [
            "Research",
            "Prototype",
        ],

        "keywords": [
            "climate",
            "hydrology",
            "flood",
            "disaster",
            "climate resilience",
        ],

        "consortium_requirement": True,
        "international_partner_required": True,
        "industry_partner_required": False,

        "matching_faculty": [
            "Dr. Rahul Sharma",
            "Dr. Meera Krishnan",
        ],
    },

    {
        "id": 2,
        "name": "AI for Earth Observation Challenge",
        "organization": "Department of Biotechnology (DBT)",
        "amount": 750000,
        "deadline": "2026-10-30",

        "fields": [
            "Computer Vision",
            "Remote Sensing",
            "Artificial Intelligence",
        ],

        "eligibility": [
            "Faculty",
            "Research Scholars",
        ],

        "research_stage": [
            "Research",
            "Prototype",
        ],

        "keywords": [
            "computer vision",
            "remote sensing",
            "satellite",
            "earth observation",
            "AI",
            "deep learning",
        ],

        "consortium_requirement": False,
        "international_partner_required": False,
        "industry_partner_required": True,

        "matching_faculty": [
            "Dr. Ananya Rao",
            "Dr. Priya Menon",
        ],
    },

    {
        "id": 3,
        "name": "Renewable Energy Innovation Fund",
        "organization": "Ministry of New and Renewable Energy (MNRE)",
        "amount": 1200000,
        "deadline": "2026-12-05",

        "fields": [
            "Renewable Energy",
            "Energy Systems",
            "Sustainable Engineering",
        ],

        "eligibility": [
            "Faculty",
            "Research Scholars",
        ],

        "research_stage": [
            "Research",
            "Prototype",
            "Deployment",
        ],

        "keywords": [
            "renewable energy",
            "solar energy",
            "energy systems",
            "energy optimization",
            "sustainable",
        ],

        "consortium_requirement": True,
        "international_partner_required": False,
        "industry_partner_required": True,

        "matching_faculty": [
            "Dr. Suresh Iyer",
        ],
    },

    {
        "id": 4,
        "name": "Genomics for Public Health Consortium",
        "organization": "Indian Council of Medical Research (ICMR)",
        "amount": 1500000,
        "deadline": "2027-01-20",

        "fields": [
            "Genomics",
            "Bioinformatics",
            "Computational Biology",
        ],

        "eligibility": [
            "Faculty",
            "Research Scholars",
        ],

        "research_stage": [
            "Research",
            "Prototype",
        ],

        "keywords": [
            "genomics",
            "bioinformatics",
            "genomic sequence",
            "machine learning",
            "disease",
            "computational biology",
        ],

        "consortium_requirement": True,
        "international_partner_required": True,
        "industry_partner_required": False,

        "matching_faculty": [
            "Dr. Kavitha Reddy",
        ],
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

TRACKING_STAGES = [
    "Recommendation",
    "Introduction",
    "Meeting",
    "Proposal",
    "Funded Project",
    "Publication",
]


TRACKING_RECORDS = [
    {
        "id": 1,
        "faculty_a": "Dr. Ananya Rao",
        "faculty_b": "Dr. Rahul Sharma",

        "external_researcher_id": None,
        "external_institution": None,

        "topic": "AI-based GLOF monitoring and early warning",
        "current_stage": "Meeting",
        "history": [
            "Recommendation",
            "Introduction",
            "Meeting",
        ],
        "last_updated": "2026-09-02",
    },

    {
        "id": 2,
        "faculty_a": "Dr. Vikram Nair",
        "faculty_b": "Dr. Kavitha Reddy",

        "external_researcher_id": None,
        "external_institution": None,

        "topic": "AI-driven genomic sequence analysis",
        "current_stage": "Introduction",
        "history": [
            "Recommendation",
            "Introduction",
        ],
        "last_updated": "2026-08-21",
    },

    {
        "id": 3,
        "faculty_a": "Dr. Priya Menon",
        "faculty_b": "Dr. Meera Krishnan",

        "external_researcher_id": None,
        "external_institution": None,

        "topic": "Satellite-based disaster risk mapping",
        "current_stage": "Proposal",
        "history": [
            "Recommendation",
            "Introduction",
            "Meeting",
            "Proposal",
        ],
        "last_updated": "2026-08-30",
    },

    {
        "id": 4,
        "faculty_a": "Dr. Suresh Iyer",
        "faculty_b": "Dr. Arjun Desai",

        "external_researcher_id": None,
        "external_institution": None,

        "topic": "Robotics-assisted renewable energy maintenance",
        "current_stage": "Recommendation",
        "history": [
            "Recommendation",
        ],
        "last_updated": "2026-09-08",
    },

    # External collaboration tracking example
    {
        "id": 5,
        "faculty_a": "Dr. Kavitha Reddy",
        "faculty_b": None,

        "external_researcher_id": 5,
        "external_institution": "National University of Singapore",

        "topic": "Cross-border bioinformatics pipeline development",
        "current_stage": "Funded Project",
        "history": [
            "Recommendation",
            "Introduction",
            "Meeting",
            "Proposal",
            "Funded Project",
        ],
        "last_updated": "2026-07-15",
    },
]


PUBLICATIONS = [
    {
        "id": 1,
        "title": "Deep Learning for Automated Detection of Objects in Satellite Imagery",
        "faculty_name": "Dr. Ananya Rao",
        "year": 2025,
        "venue": "International Conference on Computer Vision and Pattern Recognition",
        "doi": None,
    },
    {
        "id": 2,
        "title": "Vision-Based Analysis of Disaster-Affected Regions Using Deep Neural Networks",
        "faculty_name": "Dr. Ananya Rao",
        "year": 2024,
        "venue": "Journal of Intelligent Systems",
        "doi": None,
    },
    {
        "id": 3,
        "title": "Hydrological Modeling for Climate-Resilient Flood Prediction",
        "faculty_name": "Dr. Rahul Sharma",
        "year": 2025,
        "venue": "Journal of Hydrology and Climate Science",
        "doi": None,
    },
    {
        "id": 4,
        "title": "Climate Variability and Extreme Flood Events in South Asia",
        "faculty_name": "Dr. Rahul Sharma",
        "year": 2024,
        "venue": "Climate Risk Research",
        "doi": None,
    },
    {
        "id": 5,
        "title": "Satellite-Based Remote Sensing for Disaster Mapping",
        "faculty_name": "Dr. Priya Menon",
        "year": 2025,
        "venue": "Remote Sensing Applications",
        "doi": None,
    },
    {
        "id": 6,
        "title": "Signal Processing Techniques for Environmental Monitoring",
        "faculty_name": "Dr. Priya Menon",
        "year": 2024,
        "venue": "International Journal of Signal Processing",
        "doi": None,
    },
    {
        "id": 7,
        "title": "Artificial Intelligence Methods for Natural Language Understanding",
        "faculty_name": "Dr. Vikram Nair",
        "year": 2025,
        "venue": "AI and Language Technologies",
        "doi": None,
    },
    {
        "id": 8,
        "title": "Deep Learning Approaches for Multilingual Text Analysis",
        "faculty_name": "Dr. Vikram Nair",
        "year": 2024,
        "venue": "Computational Intelligence Journal",
        "doi": None,
    },
    {
        "id": 9,
        "title": "Machine Learning for Genomic Sequence Analysis",
        "faculty_name": "Dr. Kavitha Reddy",
        "year": 2025,
        "venue": "Bioinformatics and Computational Biology",
        "doi": None,
    },
    {
        "id": 10,
        "title": "Computational Methods for Disease-Related Gene Identification",
        "faculty_name": "Dr. Kavitha Reddy",
        "year": 2024,
        "venue": "Genomics Research",
        "doi": None,
    },
    {
        "id": 11,
        "title": "Optimization of Hybrid Renewable Energy Systems",
        "faculty_name": "Dr. Suresh Iyer",
        "year": 2025,
        "venue": "Renewable Energy Engineering",
        "doi": None,
    },
    {
        "id": 12,
        "title": "Thermal Performance Analysis of Solar Energy Systems",
        "faculty_name": "Dr. Suresh Iyer",
        "year": 2024,
        "venue": "Energy Systems Research",
        "doi": None,
    },
    {
        "id": 13,
        "title": "Climate Change and Disaster Risk Assessment in Vulnerable Regions",
        "faculty_name": "Dr. Meera Krishnan",
        "year": 2025,
        "venue": "Climate and Disaster Management",
        "doi": None,
    },
    {
        "id": 14,
        "title": "Data-Driven Approaches for Community Disaster Preparedness",
        "faculty_name": "Dr. Meera Krishnan",
        "year": 2024,
        "venue": "Disaster Risk Reduction Journal",
        "doi": None,
    },
    {
        "id": 15,
        "title": "Computer Vision for Autonomous Robotic Navigation",
        "faculty_name": "Dr. Arjun Desai",
        "year": 2025,
        "venue": "Robotics and Autonomous Systems",
        "doi": None,
    },
    {
        "id": 16,
        "title": "Vision-Based Navigation for Robots in Unstructured Environments",
        "faculty_name": "Dr. Arjun Desai",
        "year": 2024,
        "venue": "International Robotics Conference",
        "doi": None,
    },
]


PROJECTS = [
    {
        "id": 1,
        "title": "AI-Based Disaster Image Analysis",
        "faculty_name": "Dr. Ananya Rao",
        "description": "Development of deep learning methods for detecting and analyzing disaster-affected regions from images.",
        "research_area": "Computer Vision",
        "status": "Active",
    },
    {
        "id": 2,
        "title": "Climate-Based Flood Forecasting System",
        "faculty_name": "Dr. Rahul Sharma",
        "description": "Development of hydrological models for predicting flood risks using climate and environmental data.",
        "research_area": "Hydrology",
        "status": "Active",
    },
    {
        "id": 3,
        "title": "Satellite Disaster Monitoring Platform",
        "faculty_name": "Dr. Priya Menon",
        "description": "Use of satellite remote sensing and signal processing for monitoring disaster-affected regions.",
        "research_area": "Remote Sensing",
        "status": "Active",
    },
    {
        "id": 4,
        "title": "AI Research and Language Intelligence Platform",
        "faculty_name": "Dr. Vikram Nair",
        "description": "Development of artificial intelligence and natural language processing techniques for intelligent information systems.",
        "research_area": "Artificial Intelligence",
        "status": "Active",
    },
    {
        "id": 5,
        "title": "AI-Assisted Genomic Disease Analysis",
        "faculty_name": "Dr. Kavitha Reddy",
        "description": "Application of machine learning and bioinformatics techniques to genomic data for disease analysis.",
        "research_area": "Bioinformatics",
        "status": "Active",
    },
    {
        "id": 6,
        "title": "Smart Renewable Energy Management",
        "faculty_name": "Dr. Suresh Iyer",
        "description": "Development of intelligent systems for improving the efficiency and management of renewable energy systems.",
        "research_area": "Renewable Energy",
        "status": "Active",
    },
    {
        "id": 7,
        "title": "Climate Disaster Risk Assessment",
        "faculty_name": "Dr. Meera Krishnan",
        "description": "Assessment of climate-related disaster risks using environmental and socioeconomic information.",
        "research_area": "Disaster Risk Management",
        "status": "Active",
    },
    {
        "id": 8,
        "title": "Autonomous Disaster Response Robotics",
        "faculty_name": "Dr. Arjun Desai",
        "description": "Development of computer-vision-enabled robots for navigation and assistance during disaster response operations.",
        "research_area": "Robotics",
        "status": "Active",
    },
]