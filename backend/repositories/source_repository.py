from sqlalchemy import text

from backend.database.connection import engine


def get_source_id(source_name: str):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT id
                FROM sources
                WHERE name = :name
            """),
            {"name": source_name}
        ).fetchone()

        if not result:
            raise ValueError(f"Source not found: {source_name}")

        return result[0]