from database.connection import SessionLocal
from models.models import TrackingRecord, MoU


class ImpactAgent:
    """
    Agent responsible for measuring
    research collaboration impact.
    """

    def __init__(self):
        self.name = "Collaboration Impact Agent"

    def get_tracking_records(self):
        db = SessionLocal()

        try:
            records = db.query(TrackingRecord).all()

            return [
                {
                    "id": record.id,
                    "faculty_a": record.faculty_a,
                    "faculty_b": record.faculty_b,
                    "external_researcher_id": record.external_researcher_id,
                    "external_institution": record.external_institution,
                    "topic": record.topic,
                    "current_stage": record.current_stage,
                    "history": record.history or [],
                }
                for record in records
            ]

        finally:
            db.close()

    def get_mous(self):
        db = SessionLocal()

        try:
            mous = db.query(MoU).all()

            return [
                {
                    "id": mou.id,
                    "institution": mou.institution,
                    "status": mou.status,
                    "joint_publications": mou.joint_publications or 0,
                    "joint_projects": mou.joint_projects or 0,
                }
                for mou in mous
            ]

        finally:
            db.close()

    def calculate_impact(self):
        tracking_records = self.get_tracking_records()
        mous = self.get_mous()

        internal = [
            record
            for record in tracking_records
            if record["faculty_b"] is not None
        ]

        external = [
            record
            for record in tracking_records
            if record["external_researcher_id"] is not None
        ]

        funded_projects = [
            record
            for record in tracking_records
            if record["current_stage"] == "Funded Project"
        ]

        active_mous = [
            mou
            for mou in mous
            if mou["status"] == "Active"
        ]

        underutilized_mous = [
            mou
            for mou in mous
            if mou["status"] == "Underutilized"
        ]

        dormant_mous = [
            mou
            for mou in mous
            if mou["status"] == "Dormant"
        ]

        total_joint_publications = sum(
            mou["joint_publications"]
            for mou in mous
        )

        total_joint_projects = sum(
            mou["joint_projects"]
            for mou in mous
        )

        return {
            "total_collaborations": len(tracking_records),
            "internal_collaborations": len(internal),
            "external_collaborations": len(external),
            "funded_projects": len(funded_projects),

            "total_mous": len(mous),
            "active_mous": len(active_mous),
            "underutilized_mous": len(underutilized_mous),
            "dormant_mous": len(dormant_mous),

            "total_joint_publications": total_joint_publications,
            "total_joint_projects": total_joint_projects,

            "stage_summary": self.get_stage_summary(
                tracking_records
            ),
        }

    def get_stage_summary(self, records=None):
        if records is None:
            records = self.get_tracking_records()

        summary = {}

        for record in records:
            stage = record["current_stage"] or "Unknown"

            if stage not in summary:
                summary[stage] = 0

            summary[stage] += 1

        return summary

    def run(self):
        return self.calculate_impact()