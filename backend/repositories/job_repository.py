from sqlalchemy import text

from backend.database.connection import engine


def create_job(
    company_id,
    source_id,
    title,
    location,
    job_url,
):

    with engine.connect() as conn:

        existing = conn.execute(
            text("""
                SELECT id
                FROM jobs
                WHERE job_url = :job_url
            """),
            {"job_url": job_url}
        ).fetchone()

        if existing:
            return existing[0]

        result = conn.execute(
            text("""
                INSERT INTO jobs (
                    company_id,
                    source_id,
                    title,
                    location,
                    job_url
                )
                VALUES (
                    :company_id,
                    :source_id,
                    :title,
                    :location,
                    :job_url
                )
                RETURNING id
            """),
            {
                "company_id": company_id,
                "source_id": source_id,
                "title": title,
                "location": location,
                "job_url": job_url,
            }
        )

        job_id = result.scalar()

        conn.commit()

        return job_id