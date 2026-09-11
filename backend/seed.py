from datetime import datetime

from database.connection import SessionLocal
from models.models import (
    Faculty,
    Publication,
    Project,
    Collaboration,
    ExternalResearcher,
    FundingCall,
    MoU,
    TrackingRecord,
)

from data.mock_data import (
    FACULTY,
    PUBLICATIONS,
    PROJECTS,
    COLLABORATIONS,
    EXTERNAL_RESEARCHERS,
    FUNDING_OPPORTUNITIES,
    MOUS,
    TRACKING_RECORDS,
)


def parse_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def seed_database():
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # Clear existing seeded data
        # ---------------------------------------------------------

        db.query(TrackingRecord).delete()
        db.query(MoU).delete()
        db.query(FundingCall).delete()
        db.query(ExternalResearcher).delete()
        db.query(Collaboration).delete()
        db.query(Faculty).delete()
        db.query(Project).delete()
        db.query(Publication).delete()

        # ---------------------------------------------------------
        # FACULTY
        # ---------------------------------------------------------

        for item in FACULTY:
            faculty = Faculty(
                id=item["id"],
                name=item["name"],
                department=item["department"],
                designation=item["designation"],
                research_areas=item["research_areas"],
                publications_count=item["publications_count"],
                collaboration_count=item["collaboration_count"],
            )

            db.add(faculty)

        # ---------------------------------------------------------
        # PUBLICATIONS
        # ---------------------------------------------------------
        for item in PUBLICATIONS:
            publication = Publication(
                id=item["id"],
                title=item["title"],
                faculty_name=item["faculty_name"],
                year=item["year"],
                venue=item["venue"],
                doi=item["doi"],
            )

            db.add(publication)

        # ---------------------------------------------------------
        # PROJECTS
        # ---------------------------------------------------------
        for item in PROJECTS:
            project = Project(
                id=item["id"],
                title=item["title"],
                faculty_name=item["faculty_name"],
                description=item["description"],
                research_area=item["research_area"],
                status=item["status"],
            )

            db.add(project)

        # ---------------------------------------------------------
        # COLLABORATIONS
        # ---------------------------------------------------------

        for item in COLLABORATIONS:
            collaboration = Collaboration(
                id=item["id"],
                faculty_a=item["faculty_a"],
                faculty_b=item["faculty_b"],
                department=item["department"],
                research_areas=item["research_areas"],
                collaboration_type=item["collaboration_type"],
                collaboration_strength=item["collaboration_strength"],
            )

            db.add(collaboration)

        # ---------------------------------------------------------
        # EXTERNAL RESEARCHERS
        # ---------------------------------------------------------

        for item in EXTERNAL_RESEARCHERS:
            researcher = ExternalResearcher(
                id=item["id"],
                name=item["name"],
                institution=item["institution"],
                country=item["country"],
                research_area=item["research_area"],
                research_fit=item["research_fit"],
                network_reachability=item["network_reachability"],
                overall_score=item["overall_score"],
            )

            db.add(researcher)

        # ---------------------------------------------------------
        # FUNDING CALLS
        # ---------------------------------------------------------

        for item in FUNDING_OPPORTUNITIES:
            funding_call = FundingCall(
                id=item["id"],
                title=item["title"],
                organization=item["organization"],
                deadline=parse_date(item["deadline"]),
                research_areas=item["research_areas"],
                consortium_requirement=item["consortium_requirement"],
                international_partner_required=item[
                    "international_partner_required"
                ],
                industry_partner_required=item[
                    "industry_partner_required"
                ],
                matching_faculty=item["matching_faculty"],
            )

            db.add(funding_call)

        # ---------------------------------------------------------
        # MoUs
        # ---------------------------------------------------------

        for item in MOUS:
            mou = MoU(
                id=item["id"],
                institution=item["institution"],
                country=item["country"],
                research_area=item["research_area"],
                signed_date=parse_date(item["signed_date"]),
                last_activity=parse_date(item["last_activity"]),
                joint_publications=item["joint_publications"],
                joint_projects=item["joint_projects"],
                status=item["status"],
            )

            db.add(mou)

        # ---------------------------------------------------------
        # TRACKING RECORDS
        # ---------------------------------------------------------

        for item in TRACKING_RECORDS:
            tracking_record = TrackingRecord(
                id=item["id"],
                faculty_a=item["faculty_a"],
                faculty_b=item["faculty_b"],
                topic=item["topic"],
                current_stage=item["current_stage"],
                history=item["history"],
                last_updated=parse_date(item["last_updated"]),
            )

            db.add(tracking_record)

        # ---------------------------------------------------------
        # SAVE EVERYTHING
        # ---------------------------------------------------------

        db.commit()

        print("Database seeded successfully.")
        print(f"Faculty: {len(FACULTY)}")
        print(f"Collaborations: {len(COLLABORATIONS)}")
        print(f"External researchers: {len(EXTERNAL_RESEARCHERS)}")
        print(f"Funding calls: {len(FUNDING_OPPORTUNITIES)}")
        print(f"MoUs: {len(MOUS)}")
        print(f"Tracking records: {len(TRACKING_RECORDS)}")
        print(f"Publications: {len(PUBLICATIONS)}")
        print(f"Projects: {len(PROJECTS)}")

    except Exception as error:
        db.rollback()
        print("Error while seeding database:")
        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()