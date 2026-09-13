"""
Agent 24 - External collaboration support migration.

Adds:
1. external_researchers.email
2. collaboration_requests.target_external_researcher_id
3. makes collaboration_requests.target_faculty_id nullable
4. collaboration_response_tokens.recipient_external_researcher_id
"""

from sqlalchemy import text

from database.connection import engine


def run():

    with engine.begin() as conn:

        # ----------------------------------------------------
        # External researcher email
        # ----------------------------------------------------

        conn.execute(
            text(
                """
                ALTER TABLE external_researchers
                ADD COLUMN IF NOT EXISTS email VARCHAR(255);
                """
            )
        )

        # ----------------------------------------------------
        # External target on collaboration request
        # ----------------------------------------------------

        conn.execute(
            text(
                """
                ALTER TABLE collaboration_requests
                ADD COLUMN IF NOT EXISTS
                target_external_researcher_id INTEGER;
                """
            )
        )

        # Make internal faculty target optional
        conn.execute(
            text(
                """
                ALTER TABLE collaboration_requests
                ALTER COLUMN target_faculty_id DROP NOT NULL;
                """
            )
        )

        # Foreign key for external target
        conn.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname =
                            'fk_collaboration_requests_external_researcher'
                    ) THEN

                        ALTER TABLE collaboration_requests
                        ADD CONSTRAINT
                        fk_collaboration_requests_external_researcher
                        FOREIGN KEY (
                            target_external_researcher_id
                        )
                        REFERENCES external_researchers(id);

                    END IF;
                END
                $$;
                """
            )
        )

        # Index
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS
                ix_collaboration_requests_target_external
                ON collaboration_requests(
                    target_external_researcher_id
                );
                """
            )
        )

        # ----------------------------------------------------
        # External recipient on response token
        # ----------------------------------------------------

        conn.execute(
            text(
                """
                ALTER TABLE collaboration_response_tokens
                ADD COLUMN IF NOT EXISTS
                recipient_external_researcher_id INTEGER;
                """
            )
        )

        # Foreign key
        conn.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname =
                            'fk_response_tokens_external_researcher'
                    ) THEN

                        ALTER TABLE collaboration_response_tokens
                        ADD CONSTRAINT
                        fk_response_tokens_external_researcher
                        FOREIGN KEY (
                            recipient_external_researcher_id
                        )
                        REFERENCES external_researchers(id);

                    END IF;
                END
                $$;
                """
            )
        )

        # Index
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS
                ix_response_tokens_external_researcher
                ON collaboration_response_tokens(
                    recipient_external_researcher_id
                );
                """
            )
        )

    print(
        "Agent 24 v3 migration completed successfully."
    )


if __name__ == "__main__":
    run()