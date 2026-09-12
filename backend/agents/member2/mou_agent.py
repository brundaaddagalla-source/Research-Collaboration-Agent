from database.connection import SessionLocal
from models.models import MoU


class MoUAgent:
    """
    Agent responsible for analyzing
    institutional MoU relationships.
    """

    def __init__(self):
        self.name = "MoU Intelligence Agent"

    def get_mous(self):
        """
        Get MoU records from the database.
        """

        db = SessionLocal()

        try:
            mou_records = db.query(MoU).all()

            mous = []

            for mou in mou_records:
                mous.append({
                    "id": mou.id,
                    "institution": mou.institution,
                    "country": mou.country,
                    "research_area": mou.research_area,
                    "signed_date": (
                        mou.signed_date.isoformat()
                        if mou.signed_date
                        else None
                    ),
                    "last_activity": (
                        mou.last_activity.isoformat()
                        if mou.last_activity
                        else None
                    ),
                    "joint_publications": mou.joint_publications or 0,
                    "joint_projects": mou.joint_projects or 0,
                    "status": mou.status,
                })

            return mous

        finally:
            db.close()

    def get_active_mous(self):
        """
        Return currently active MoU relationships.
        """

        mous = self.get_mous()

        return [
            mou
            for mou in mous
            if mou["status"] == "Active"
        ]

    def get_underutilized_mous(self):
        """
        Return MoUs that may have collaboration potential.
        """

        mous = self.get_mous()

        return [
            mou
            for mou in mous
            if mou["status"] in [
                "Underutilized",
                "Dormant"
            ]
        ]

    def run(self):
        """
        Run MoU intelligence analysis.
        """

        mous = self.get_mous()

        active = [
            mou for mou in mous
            if mou["status"] == "Active"
        ]

        underutilized = [
            mou for mou in mous
            if mou["status"] == "Underutilized"
        ]

        dormant = [
            mou for mou in mous
            if mou["status"] == "Dormant"
        ]

        return {
            "total_mous": len(mous),
            "active_mous": active,
            "underutilized_mous": underutilized,
            "dormant_mous": dormant,
            "all_mous": mous,
        }