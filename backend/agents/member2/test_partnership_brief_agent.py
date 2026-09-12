from agents.member2.partnership_brief_agent import (
    PartnershipBriefAgent
)


def main():

    print("=" * 60)
    print("PARTNERSHIP BRIEF AGENT TEST")
    print("=" * 60)

    faculty = {
        "name": "Ananya Rao",
        "department": "Computer Science",
        "research_areas": [
            "Artificial Intelligence",
            "Remote Sensing",
            "Disaster Management"
        ],
        "publications": [
            "AI-based remote sensing for disaster monitoring"
        ],
        "projects": [
            "AI-based GLOF monitoring"
        ],
    }

    external_researcher = {
        "name": "Dr. Kenji Watanabe",
        "institution": "Tokyo Institute of Technology",
        "country": "Japan",
        "research_interests": [
            "Computer Vision",
            "Artificial Intelligence",
            "Deep Learning",
            "Robotics"
        ],
        "skills": [
            "Python",
            "Deep Learning",
            "Computer Vision",
            "Image Processing"
        ],
        "research_area": "Computer Vision",
        "research_fit": 92,
        "network_reachability": "High",
    }

    funding = {
        "name": "AI for Earth Observation Challenge",
        "organization": "DBT",
        "amount": 750000,
        "deadline": "2026-10-30",
        "fields": [
            "Computer Vision",
            "Remote Sensing",
            "Artificial Intelligence"
        ],
    }

    mou = {
        "institution": "Tokyo Institute of Technology",
        "country": "Japan",
        "research_area": "Computer Vision",
        "status": "Active",
        "joint_publications": 6,
        "joint_projects": 2,
    }

    agent = PartnershipBriefAgent()

    result = agent.run(
        faculty=faculty,
        external_researcher=external_researcher,
        funding=funding,
        mou=mou
    )

    print("\n----------------------------------------")
    print("GENERATED PARTNERSHIP BRIEF")
    print("----------------------------------------")

    print(result["brief"])

    print("\n========================================")
    print("PARTNERSHIP BRIEF TEST PASSED")
    print("========================================")


if __name__ == "__main__":
    main()