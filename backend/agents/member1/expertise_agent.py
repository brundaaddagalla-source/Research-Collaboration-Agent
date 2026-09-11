# from database.connection import SessionLocal
# from models.models import Faculty, Publication, Project


# def build_faculty_profile(faculty):
#     """
#     Build a rich research profile for one faculty member.

#     Profile includes:
#     - Department
#     - Research areas
#     - Publications
#     - Projects
#     """

#     db = SessionLocal()

#     try:
#         publications = (
#             db.query(Publication)
#             .filter(Publication.faculty_name == faculty.name)
#             .all()
#         )

#         projects = (
#             db.query(Project)
#             .filter(Project.faculty_name == faculty.name)
#             .all()
#         )

#         research_areas = faculty.research_areas or []

#         if isinstance(research_areas, list):
#             research_area_text = ", ".join(research_areas)
#         else:
#             research_area_text = str(research_areas)

#         publication_text = "\n".join(
#             f"- {publication.title}"
#             for publication in publications
#         )

#         project_text = "\n".join(
#             f"- {project.title}: {project.description}"
#             for project in projects
#         )

#         profile = (
#             f"Faculty: {faculty.name}\n"
#             f"Department: {faculty.department}\n"
#             f"Research Areas: {research_area_text}\n\n"
#             f"Publications:\n"
#             f"{publication_text or '- None available'}\n\n"
#             f"Projects:\n"
#             f"{project_text or '- None available'}"
#         )

#         return profile

#     finally:
#         db.close()


# def get_all_faculty_profiles():
#     """
#     Build research profiles for all faculty members.
#     """

#     db = SessionLocal()

#     try:
#         faculty_list = db.query(Faculty).all()

#         profiles = []

#         for faculty in faculty_list:
#             profile = build_faculty_profile(faculty)

#             profiles.append(
#                 {
#                     "faculty_id": faculty.id,
#                     "name": faculty.name,
#                     "department": faculty.department,
#                     "profile": profile,
#                 }
#             )

#         return profiles

#     finally:
#         db.close()

from database.connection import SessionLocal
from models.models import Faculty, Publication, Project


def build_faculty_profile(faculty):
    """
    Build a rich research profile for one faculty member.

    Profile includes:
    - Department
    - Research areas
    - Publications
    - Projects
    """

    db = SessionLocal()

    try:
        publications = (
            db.query(Publication)
            .filter(Publication.faculty_name == faculty.name)
            .all()
        )

        projects = (
            db.query(Project)
            .filter(Project.faculty_name == faculty.name)
            .all()
        )

        research_areas = faculty.research_areas or []

        if isinstance(research_areas, list):
            research_area_text = ", ".join(research_areas)
        else:
            research_area_text = str(research_areas)

        publication_text = "\n".join(
            f"- {publication.title}"
            for publication in publications
        )

        project_text = "\n".join(
            f"- {project.title}: {project.description}"
            for project in projects
        )

        profile = (
            f"Faculty: {faculty.name}\n"
            f"Department: {faculty.department}\n"
            f"Research Areas: {research_area_text}\n\n"
            f"Publications:\n"
            f"{publication_text or '- None available'}\n\n"
            f"Projects:\n"
            f"{project_text or '- None available'}"
        )

        return profile

    finally:
        db.close()


def get_all_faculty_profiles():
    """
    Build research profiles for all faculty members.
    """

    db = SessionLocal()

    try:
        faculty_list = db.query(Faculty).all()

        profiles = []

        for faculty in faculty_list:
            profile = build_faculty_profile(faculty)

            profiles.append(
                {
                    "faculty_id": faculty.id,
                    "name": faculty.name,
                    "department": faculty.department,
                    "profile": profile,
                }
            )

        return profiles

    finally:
        db.close()


def get_all_faculty_evidence():
    """
    Build structured research evidence for every faculty member.

    This provides the collaboration engine with:
    - Research areas
    - Publications
    - Projects
    """

    db = SessionLocal()

    try:
        faculty_list = db.query(Faculty).all()

        evidence = {}

        for faculty in faculty_list:

            publications = (
                db.query(Publication)
                .filter(
                    Publication.faculty_name
                    == faculty.name
                )
                .all()
            )

            projects = (
                db.query(Project)
                .filter(
                    Project.faculty_name
                    == faculty.name
                )
                .all()
            )

            research_areas = (
                faculty.research_areas or []
            )

            evidence[faculty.id] = {
                "research_areas": research_areas,

                "publications": [
                    {
                        "title": publication.title,
                        "year": publication.year,
                        "venue": publication.venue,
                        "doi": publication.doi,
                    }
                    for publication in publications
                ],

                "projects": [
                    {
                        "title": project.title,
                        "description": project.description,
                        "research_area": project.research_area,
                        "status": project.status,
                    }
                    for project in projects
                ],
            }

        return evidence

    finally:
        db.close()