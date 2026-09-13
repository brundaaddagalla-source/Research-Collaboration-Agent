# from datetime import datetime

# from database.connection import SessionLocal

# from models.models import (
#     Faculty,
#     Publication,
#     Project,
#     Collaboration,
#     ExternalResearcher,
#     FundingCall,
#     MoU,
#     TrackingRecord,
#     FacultyCredential,
# )

# from data.mock_data import (
#     FACULTY,
#     PUBLICATIONS,
#     PROJECTS,
#     COLLABORATIONS,
#     EXTERNAL_RESEARCHERS,
#     FUNDING_OPPORTUNITIES,
#     MOUS,
#     TRACKING_RECORDS,
# )

# from services.auth_service import hash_password


# # NOTE (Agent 24 v3):
# # FacultyResearchDocument, CollaborationRequest and
# # CollaborationResponseToken are intentionally NOT imported/deleted/reseeded
# # here. They hold real faculty-generated data (uploads, collaboration
# # requests, email tokens) and must survive re-running this mock-data seed
# # script.
# #
# # Faculty rows are deleted/recreated with the SAME ids each run, so
# # foreign keys from those tables remain valid.
# #
# # External researchers are mock/reference data and are reseeded each run.
# # Their email field is now supported for external collaboration requests.


# # ============================================================
# # COMMON FACULTY GRID
# # ============================================================

# # Every faculty member uses the SAME grid values.

# COMMON_GRID = {
#     "G1": "A7K2",
#     "G2": "M4P9",
#     "G3": "X8Q1",
#     "G4": "B6R3",
#     "G5": "N2T8",
#     "G6": "K5W4",
#     "G7": "P9C6",
#     "G8": "D3Y7",
#     "G9": "H8L2",
#     "G10": "Q4M5",
#     "G11": "R7V1",
#     "G12": "F2Z8",
#     "G13": "T6N3",
#     "G14": "W9B4",
#     "G15": "C5K7",
#     "G16": "J1P6",
# }


# # ============================================================
# # DATABASE
# # ============================================================

# db = SessionLocal()

# try:

#     # ========================================================
#     # CLEAR EXISTING DATA
#     # ========================================================

#     db.query(TrackingRecord).delete()
#     db.query(Collaboration).delete()
#     db.query(FacultyCredential).delete()
#     db.query(Faculty).delete()
#     db.query(Project).delete()
#     db.query(Publication).delete()

#     db.commit()


#     # ========================================================
#     # FACULTY
#     # ========================================================

#     for item in FACULTY:

#         faculty = Faculty(
#             id=item["id"],
#             name=item["name"],
#             email=item["email"],
#             department=item["department"],
#             designation=item["designation"],
#             research_areas=item["research_areas"],
#             publications_count=item["publications_count"],
#             collaboration_count=item["collaboration_count"],
#         )

#         db.add(faculty)

#     db.flush()


#     # ========================================================
#     # FACULTY CREDENTIALS
#     # ========================================================

#     # Credentials are generated directly from FACULTY.
#     #
#     # Faculty IDs:
#     #
#     # 10243 - Dr. Ananya Rao
#     # 22345 - Dr. Rahul Sharma
#     # 31452 - Dr. Priya Menon
#     # 42561 - Dr. Vikram Nair
#     # 53672 - Dr. Kavitha Reddy
#     # 64783 - Dr. Suresh Iyer
#     # 75894 - Dr. Meera Krishnan
#     # 86915 - Dr. Arjun Desai
#     #
#     # Default development password:
#     # faculty123

#     for item in FACULTY:

#         credential = FacultyCredential(
#             faculty_id=str(item["id"]),
#             name=item["name"],
#             password_hash=hash_password("faculty123"),
#             grid_secret=COMMON_GRID.copy(),
#         )

#         db.add(credential)


#     # ========================================================
#     # PUBLICATIONS
#     # ========================================================

#     for item in PUBLICATIONS:

#         publication = Publication(
#             **item
#         )

#         db.add(publication)


#     # ========================================================
#     # PROJECTS
#     # ========================================================

#     for item in PROJECTS:

#         project = Project(
#             **item
#         )

#         db.add(project)


#     # ========================================================
#     # COLLABORATIONS
#     # ========================================================

#     for item in COLLABORATIONS:

#         collaboration = Collaboration(
#             **item
#         )

#         db.add(collaboration)


#     # ========================================================
#     # EXTERNAL RESEARCHERS
#     # ========================================================

#     # External researchers now include:
#     #
#     # email
#     #
#     # This allows Agent 24 to send collaboration invitations
#     # directly to external researchers.
#     #
#     # The email values come from data/mock_data.py.

#     for item in EXTERNAL_RESEARCHERS:
#         researcher = (
#             db.query(ExternalResearcher)
#             .filter(ExternalResearcher.id == item["id"])
#             .first()
#         )

#         if researcher:
#             researcher.name = item["name"]
#             researcher.institution = item.get("institution")
#             researcher.country = item.get("country")
#             researcher.email = item.get("email")
#             researcher.research_interests = item.get("research_interests", [])
#             researcher.skills = item.get("skills", [])
#             researcher.research_area = item.get("research_area")
#             researcher.research_fit = item.get("research_fit")
#             researcher.network_reachability = item.get("network_reachability")
#             researcher.overall_score = item.get("overall_score")
#         else:
#             researcher = ExternalResearcher(
#                 id=item["id"],
#                 name=item["name"],
#                 institution=item.get("institution"),
#                 country=item.get("country"),
#                 email=item.get("email"),
#                 research_interests=item.get("research_interests", []),
#                 skills=item.get("skills", []),
#                 research_area=item.get("research_area"),
#                 research_fit=item.get("research_fit"),
#                 network_reachability=item.get("network_reachability"),
#                 overall_score=item.get("overall_score"),
#             )
#             db.add(researcher)


    


#     # ========================================================
#     # TRACKING RECORDS
#     # ========================================================

#     for item in TRACKING_RECORDS:

#         tracking_record = TrackingRecord(
#             **item
#         )

#         db.add(tracking_record)


#     # ========================================================
#     # COMMIT
#     # ========================================================

#     db.commit()


#     # ========================================================
#     # SUCCESS MESSAGE
#     # ========================================================

#     print("Database seeded successfully.")

#     print(f"Faculty: {len(FACULTY)}")
#     print(f"Faculty credentials: {len(FACULTY)}")
#     print(f"Publications: {len(PUBLICATIONS)}")
#     print(f"Projects: {len(PROJECTS)}")
#     print(f"Collaborations: {len(COLLABORATIONS)}")

#     print(
#         f"External researchers: "
#         f"{len(EXTERNAL_RESEARCHERS)}"
#     )

#     print(
#         f"Funding calls: "
#         f"{len(FUNDING_OPPORTUNITIES)}"
#     )

#     print(f"MoUs: {len(MOUS)}")

#     print(
#         f"Tracking records: "
#         f"{len(TRACKING_RECORDS)}"
#     )

#     print()

#     print("Faculty login IDs:")

#     for item in FACULTY:

#         print(
#             f'{item["id"]} - {item["name"]}'
#         )

#     print()

#     print("External researchers:")

#     for item in EXTERNAL_RESEARCHERS:

#         print(
#             f'{item["id"]} - '
#             f'{item["name"]} - '
#             f'{item.get("email", "No email")}'
#         )

#     print()

#     print("Default password: faculty123")
#     print("Grid positions: G1-G16")
#     print("Grid values: Common for all faculty")


# except Exception as e:

#     db.rollback()

#     print("Database seeding failed.")
#     print(f"Error: {e}")

#     raise


# finally:

#     db.close()

from database.connection import SessionLocal

from models.models import (
    Faculty,
    Publication,
    Project,
    Collaboration,
    ExternalResearcher,
    FacultyCredential,
    TrackingRecord,
)

from data.mock_data import (
    FACULTY,
    PUBLICATIONS,
    PROJECTS,
    COLLABORATIONS,
    EXTERNAL_RESEARCHERS,
    TRACKING_RECORDS,
)

from services.auth_service import hash_password


# ============================================================
# NOTE (Agent 24 v3)
# ============================================================
#
# This seed refreshes mock/reference data while preserving
# faculty-generated data.
#
# The following tables are NOT deleted:
#
# - FacultyResearchDocument
# - CollaborationRequest
# - CollaborationResponseToken
# - FundingCall
# - MoU
#
# Faculty rows are UPDATED in place using their existing IDs.
# This is important because other tables contain foreign keys
# pointing to Faculty.
#
# External researchers are also UPDATED in place instead of
# being deleted/recreated, so external collaboration requests
# remain valid.
#
# Tracking records are still refreshed from TRACKING_RECORDS.
#
# ============================================================


# ============================================================
# COMMON FACULTY GRID
# ============================================================

# Every faculty member uses the SAME grid values.

COMMON_GRID = {
    "G1": "A7K2",
    "G2": "M4P9",
    "G3": "X8Q1",
    "G4": "B6R3",
    "G5": "N2T8",
    "G6": "K5W4",
    "G7": "P9C6",
    "G8": "D3Y7",
    "G9": "H8L2",
    "G10": "Q4M5",
    "G11": "R7V1",
    "G12": "F2Z8",
    "G13": "T6N3",
    "G14": "W9B4",
    "G15": "C5K7",
    "G16": "J1P6",
}


# ============================================================
# DATABASE
# ============================================================

db = SessionLocal()

try:

    # ========================================================
    # CLEAR ONLY SAFE MOCK DATA
    # ========================================================

    # Tracking records are mock/reference data.
    db.query(TrackingRecord).delete()

    # Collaboration grid/reference data.
    db.query(Collaboration).delete()

    # Faculty credentials can safely be recreated because
    # they reference the same faculty IDs.
    db.query(FacultyCredential).delete()

    # Publications and projects are mock/reference data.
    db.query(Project).delete()
    db.query(Publication).delete()

    db.commit()


    # ========================================================
    # FACULTY
    # ========================================================

    # IMPORTANT:
    # Do NOT delete Faculty rows.
    #
    # FacultyResearchDocument, CollaborationRequest and other
    # tables contain foreign keys pointing to these IDs.
    #
    # Instead, update existing rows or create them if missing.

    for item in FACULTY:

        faculty = (
            db.query(Faculty)
            .filter(Faculty.id == item["id"])
            .first()
        )

        if faculty:

            faculty.name = item["name"]
            faculty.email = item["email"]
            faculty.department = item["department"]
            faculty.designation = item["designation"]
            faculty.research_areas = item["research_areas"]
            faculty.publications_count = item["publications_count"]
            faculty.collaboration_count = item["collaboration_count"]

        else:

            faculty = Faculty(
                id=item["id"],
                name=item["name"],
                email=item["email"],
                department=item["department"],
                designation=item["designation"],
                research_areas=item["research_areas"],
                publications_count=item["publications_count"],
                collaboration_count=item["collaboration_count"],
            )

            db.add(faculty)

    db.flush()


    # ========================================================
    # FACULTY CREDENTIALS
    # ========================================================

    # Credentials are regenerated from FACULTY.

    for item in FACULTY:

        credential = FacultyCredential(
            faculty_id=str(item["id"]),
            name=item["name"],
            password_hash=hash_password("faculty123"),
            grid_secret=COMMON_GRID.copy(),
        )

        db.add(credential)


    # ========================================================
    # PUBLICATIONS
    # ========================================================

    for item in PUBLICATIONS:

        publication = Publication(
            **item
        )

        db.add(publication)


    # ========================================================
    # PROJECTS
    # ========================================================

    for item in PROJECTS:

        project = Project(
            **item
        )

        db.add(project)


    # ========================================================
    # COLLABORATIONS
    # ========================================================

    for item in COLLABORATIONS:

        collaboration = Collaboration(
            **item
        )

        db.add(collaboration)


    # ========================================================
    # EXTERNAL RESEARCHERS
    # ========================================================

    # External researchers are updated in place.
    #
    # This preserves their IDs because CollaborationRequest
    # and CollaborationResponseToken may reference them.

    for item in EXTERNAL_RESEARCHERS:

        researcher = (
            db.query(ExternalResearcher)
            .filter(ExternalResearcher.id == item["id"])
            .first()
        )

        if researcher:

            researcher.name = item["name"]
            researcher.institution = item.get("institution")
            researcher.country = item.get("country")
            researcher.email = item.get("email")
            researcher.research_interests = item.get(
                "research_interests",
                [],
            )
            researcher.skills = item.get(
                "skills",
                [],
            )
            researcher.research_area = item.get(
                "research_area"
            )
            researcher.research_fit = item.get(
                "research_fit"
            )
            researcher.network_reachability = item.get(
                "network_reachability"
            )
            researcher.overall_score = item.get(
                "overall_score"
            )

        else:

            researcher = ExternalResearcher(
                id=item["id"],
                name=item["name"],
                institution=item.get("institution"),
                country=item.get("country"),
                email=item.get("email"),
                research_interests=item.get(
                    "research_interests",
                    [],
                ),
                skills=item.get(
                    "skills",
                    [],
                ),
                research_area=item.get(
                    "research_area"
                ),
                research_fit=item.get(
                    "research_fit"
                ),
                network_reachability=item.get(
                    "network_reachability"
                ),
                overall_score=item.get(
                    "overall_score"
                ),
            )

            db.add(researcher)


    # ========================================================
    # TRACKING RECORDS
    # ========================================================

    for item in TRACKING_RECORDS:

        tracking_record = TrackingRecord(
            **item
        )

        db.add(tracking_record)


    # ========================================================
    # COMMIT
    # ========================================================

    db.commit()


    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    print("Database seeded successfully.")

    print(f"Faculty: {len(FACULTY)}")
    print(f"Faculty credentials: {len(FACULTY)}")
    print(f"Publications: {len(PUBLICATIONS)}")
    print(f"Projects: {len(PROJECTS)}")
    print(f"Collaborations: {len(COLLABORATIONS)}")
    print(
        f"External researchers: "
        f"{len(EXTERNAL_RESEARCHERS)}"
    )
    print(
        "Funding calls: preserved"
    )
    print(
        "MoUs: preserved"
    )
    print(
        f"Tracking records: "
        f"{len(TRACKING_RECORDS)}"
    )

    print()

    print("Faculty login IDs:")

    for item in FACULTY:

        print(
            f'{item["id"]} - {item["name"]}'
        )

    print()

    print("External researchers:")

    for item in EXTERNAL_RESEARCHERS:

        print(
            f'{item["id"]} - '
            f'{item["name"]} - '
            f'{item.get("email", "No email")}'
        )

    print()

    print("Default password: faculty123")
    print("Grid positions: G1-G16")
    print("Grid values: Common for all faculty")

    print()
    print("Preserved:")
    print("- Faculty research documents")
    print("- Collaboration requests")
    print("- Collaboration response tokens")
    print("- Funding calls")
    print("- MoUs")


except Exception as e:

    db.rollback()

    print("Database seeding failed.")
    print(f"Error: {e}")

    raise


finally:

    db.close()