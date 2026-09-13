"""
Agent 24 v2 - safe schema migration for the existing Neon database.

This project has no Alembic set up, so per the task instructions this
script is the "safest existing project approach for this prototype":
it inspects what's already in the database and only adds what's
missing. It never drops a table and never deletes a row.

Run once, before `python seed.py`:

    python database/migrate_agent24_v2.py

What it does, in order:

1. Faculty.email
   - Adds the column if it doesn't exist yet (as NULLable first -
     you cannot add a NOT NULL column to a table that already has
     rows without a default/backfill).
   - Backfills the 8 known faculty emails (data/mock_data.py) by
     matching on Faculty.id.
   - Only if every existing faculty row now has an email does it
     apply the final NOT NULL + UNIQUE constraint that
     models.models.Faculty declares. If some other/unexpected
     faculty row has no matching email, it stops and tells you
     exactly which id is missing rather than guessing a value.

2. New tables
   - faculty_research_documents
   - collaboration_requests
   - collaboration_response_tokens
   Created via Base.metadata.create_all(), which only creates tables
   that don't exist yet - it does not touch faculty, publications,
   projects, collaborations, external_researchers, funding_calls,
   mous, tracking_records or faculty_credentials.
"""

from sqlalchemy import text

from database.connection import engine, Base
from models import models  # noqa: F401 - registers all models on Base
from data.mock_data import FACULTY


EMAIL_BY_ID = {item["id"]: item["email"] for item in FACULTY}


def _column_exists(conn, table, column):
    result = conn.execute(
        text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = :table AND column_name = :column"
        ),
        {"table": table, "column": column},
    )
    return result.first() is not None


def migrate_faculty_email():
    with engine.begin() as conn:
        if not _column_exists(conn, "faculty", "email"):
            print("Adding faculty.email column (nullable)...")
            conn.execute(text("ALTER TABLE faculty ADD COLUMN email VARCHAR(255)"))
        else:
            print("faculty.email already exists - skipping ADD COLUMN.")

        rows = conn.execute(text("SELECT id, email FROM faculty")).fetchall()

        missing_mapping = []
        for row in rows:
            if row.email:
                continue
            email = EMAIL_BY_ID.get(row.id)
            if email is None:
                missing_mapping.append(row.id)
                continue
            conn.execute(
                text("UPDATE faculty SET email = :email WHERE id = :id"),
                {"email": email, "id": row.id},
            )
            print(f"Backfilled email for faculty id {row.id}: {email}")

        if missing_mapping:
            print(
                "WARNING: could not backfill an email for faculty id(s) "
                f"{missing_mapping} - no entry in data/mock_data.py FACULTY. "
                "Add one, or set faculty.email manually, then re-run this "
                "script. NOT NULL constraint was NOT applied."
            )
            return

        # Every row now has an email - safe to enforce NOT NULL + UNIQUE.
        already_not_null = conn.execute(
            text(
                "SELECT is_nullable FROM information_schema.columns "
                "WHERE table_name = 'faculty' AND column_name = 'email'"
            )
        ).scalar()

        if already_not_null == "YES":
            print("Applying NOT NULL constraint on faculty.email...")
            conn.execute(text("ALTER TABLE faculty ALTER COLUMN email SET NOT NULL"))

        has_unique = conn.execute(
            text(
                "SELECT 1 FROM pg_constraint WHERE conname = 'faculty_email_key'"
            )
        ).first()
        if not has_unique:
            print("Applying UNIQUE constraint on faculty.email...")
            conn.execute(
                text("ALTER TABLE faculty ADD CONSTRAINT faculty_email_key UNIQUE (email)")
            )

        print("faculty.email is backfilled and constrained.")


def create_new_tables():
    print("Creating any missing Agent 24 v2 tables "
          "(faculty_research_documents, collaboration_requests, "
          "collaboration_response_tokens)...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    migrate_faculty_email()
    create_new_tables()
    print("\nMigration complete.")