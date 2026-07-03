from sqlalchemy import text

from backend.database.connection import engine


def get_or_create_company(company_name: str):

    with engine.connect() as conn:

        existing = conn.execute(
            text("""
                SELECT id
                FROM companies
                WHERE name = :name
            """),
            {"name": company_name}
        ).fetchone()

        if existing:
            return existing[0]

        result = conn.execute(
            text("""
                INSERT INTO companies(name)
                VALUES(:name)
                RETURNING id
            """),
            {"name": company_name}
        )

        company_id = result.scalar()

        conn.commit()

        return company_id