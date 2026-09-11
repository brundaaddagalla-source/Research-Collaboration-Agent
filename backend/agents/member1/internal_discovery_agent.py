from database.connection import SessionLocal

from models.models import (
    Collaboration,
    FundingCall,
    MoU,
)

from agents.member1.expertise_agent import (
    get_all_faculty_profiles,
    get_all_faculty_evidence,
)

from agents.member1.scoring_agent import (
    score_opportunities,
)

from algorithms.collaboration_matching import (
    generate_embeddings,
    build_expertise_evidence,
    build_collaboration_graph,
    find_complementary_faculty,
)


def prepare_collaborations(faculty_profiles):
    """
    Convert the current database collaboration records.

    Database stores faculty names.

    Matching engine uses faculty IDs.
    """

    name_to_id = {
        faculty["name"]: faculty["faculty_id"]
        for faculty in faculty_profiles
    }

    db = SessionLocal()

    try:
        collaborations = (
            db.query(Collaboration)
            .all()
        )

        converted = []

        for collaboration in collaborations:

            faculty_a_id = name_to_id.get(
                collaboration.faculty_a
            )

            faculty_b_id = name_to_id.get(
                collaboration.faculty_b
            )

            if faculty_a_id is None:
                continue

            if faculty_b_id is None:
                continue

            converted.append(
                {
                    "faculty_a_id":
                        faculty_a_id,

                    "faculty_b_id":
                        faculty_b_id,

                    "faculty_a":
                        collaboration.faculty_a,

                    "faculty_b":
                        collaboration.faculty_b,
                }
            )

        return converted

    finally:
        db.close()


def prepare_evidence(faculty_evidence):
    """
    Convert raw database evidence into the format
    expected by collaboration_matching.py.
    """

    evidence_by_faculty_id = {}

    for faculty_id, data in faculty_evidence.items():

        evidence_by_faculty_id[
            faculty_id
        ] = build_expertise_evidence(
            faculty_id=faculty_id,

            research_areas=data[
                "research_areas"
            ],

            publications=data[
                "publications"
            ],

            projects=data[
                "projects"
            ],
        )

    return evidence_by_faculty_id


def prepare_funding_calls():
    """
    Load funding opportunities from the database.
    """

    db = SessionLocal()

    try:
        funding_calls = (
            db.query(FundingCall)
            .all()
        )

        return [
            {
                "id": call.id,
                "title": call.title,
                "organization":
                    getattr(
                        call,
                        "organization",
                        None,
                    ),
                "deadline":
                    getattr(
                        call,
                        "deadline",
                        None,
                    ),
                "research_areas":
                    getattr(
                        call,
                        "research_areas",
                        [],
                    ),
            }
            for call in funding_calls
        ]

    finally:
        db.close()


def prepare_mous():
    """
    Load institutional MoUs.

    Mainly useful for external collaboration.
    """

    db = SessionLocal()

    try:
        mous = (
            db.query(MoU)
            .all()
        )

        return [
            {
                "id": mou.id,

                "partner_institution":
                    getattr(
                        mou,
                        "partner_institution",
                        None,
                    ),

                "country":
                    getattr(
                        mou,
                        "country",
                        None,
                    ),

                "status":
                    getattr(
                        mou,
                        "status",
                        None,
                    ),
            }
            for mou in mous
        ]

    finally:
        db.close()


def discover_internal_collaborations(
    faculty_name,
    top_k=5,
):
    """
    Discover new internal collaboration opportunities.

    Complete pipeline:

        Faculty
          ↓
        Research profiles
          ↓
        Embeddings
          ↓
        Research evidence
          ↓
        Collaboration network
          ↓
        Funding
          ↓
        Ranked opportunities
    """

    # --------------------------------------------------
    # 1. Faculty profiles
    # --------------------------------------------------

    profiles = (
        get_all_faculty_profiles()
    )

    # --------------------------------------------------
    # 2. Faculty evidence
    # --------------------------------------------------

    faculty_evidence = (
        get_all_faculty_evidence()
    )

    evidence_by_faculty_id = (
        prepare_evidence(
            faculty_evidence
        )
    )

    # --------------------------------------------------
    # 3. Generate embeddings
    # --------------------------------------------------

    embeddings = (
        generate_embeddings(
            profiles
        )
    )

    # --------------------------------------------------
    # 4. Existing collaborations
    # --------------------------------------------------

    collaborations = (
        prepare_collaborations(
            profiles
        )
    )

    # --------------------------------------------------
    # 5. Collaboration graph
    # --------------------------------------------------

    graph = (
        build_collaboration_graph(
            collaborations
        )
    )

    # --------------------------------------------------
    # 6. Funding
    # --------------------------------------------------

    funding_calls = (
        prepare_funding_calls()
    )

    # --------------------------------------------------
    # 7. MoUs
    # --------------------------------------------------

    mous = prepare_mous()

    # --------------------------------------------------
    # 8. Find opportunities
    # --------------------------------------------------

    opportunities = (
        find_complementary_faculty(
            profiles=profiles,
            embeddings=embeddings,
            faculty_name=faculty_name,
            evidence_by_faculty_id=
                evidence_by_faculty_id,
            graph=graph,
            funding_calls=funding_calls,
            mous=mous,
            collaborations=collaborations,
            top_k=top_k,
        )
    )

    # --------------------------------------------------
    # 9. Score and rank opportunities
    # --------------------------------------------------

    scored_opportunities = (
        score_opportunities(
            opportunities
        )
    )

    return scored_opportunities