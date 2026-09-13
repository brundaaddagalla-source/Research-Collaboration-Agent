from database.connection import SessionLocal
from models.models import TrackingRecord


class TrackingAgent:
    """
    Agent responsible for tracking
    research collaboration progress.
    """

    def __init__(self):
        self.name = "Collaboration Tracking Agent"

    def get_tracking_records(self):
        """
        Get collaboration tracking records from the database.
        """

        db = SessionLocal()

        try:
            records = db.query(TrackingRecord).all()

            tracking_records = []

            for record in records:
                tracking_records.append({
                    "id": record.id,
                    "faculty_a": record.faculty_a,
                    "faculty_b": record.faculty_b,
                    "external_researcher_id": (
                        record.external_researcher_id
                    ),
                    "external_institution": (
                        record.external_institution
                    ),
                    "topic": record.topic,
                    "current_stage": record.current_stage,
                    "history": record.history or [],
                    "last_updated": (
                        record.last_updated.isoformat()
                        if record.last_updated
                        else None
                    ),
                })

            return tracking_records

        finally:
            db.close()

    def get_internal_collaborations(self):
        """
        Return internal collaboration records.
        """

        records = self.get_tracking_records()

        return [
            record
            for record in records
            if record["faculty_b"] is not None
        ]

    def get_external_collaborations(self):
        """
        Return external collaboration records.
        """

        records = self.get_tracking_records()

        return [
            record
            for record in records
            if record["external_researcher_id"] is not None
        ]

    def get_stage_summary(self):
        """
        Count collaborations at each stage.
        """

        records = self.get_tracking_records()

        summary = {}

        for record in records:

            stage = record["current_stage"] or "Unknown"

            if stage not in summary:
                summary[stage] = 0

            summary[stage] += 1

        return summary

    def run(self):
        """
        Run collaboration tracking analysis.
        """

        records = self.get_tracking_records()

        internal = [
            record
            for record in records
            if record["faculty_b"] is not None
        ]

        external = [
            record
            for record in records
            if record["external_researcher_id"] is not None
        ]

        return {
            "total_collaborations": len(records),
            "internal_collaborations": internal,
            "external_collaborations": external,
            "stage_summary": self.get_stage_summary(),
            "all_records": records,
        }