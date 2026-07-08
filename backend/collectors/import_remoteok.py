import requests

from backend.services.job_filter import is_relevant_job
from backend.repositories.company_repository import get_or_create_company
from backend.repositories.job_repository import create_job
from backend.repositories.source_repository import get_source_id


REMOTEOK_API = "https://remoteok.com/api"


def fetch_jobs():

    response = requests.get(
        REMOTEOK_API,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    return response.json()


def main():

    source_id = get_source_id("RemoteOK")

    jobs = fetch_jobs()

    inserted = 0

    for job in jobs[1:]:

        #if not is_relevant_job(job):
        #    continue

        company_name = job.get("company")

        if not company_name:
            continue

        company_id = get_or_create_company(company_name)

        create_job(
            company_id=company_id,
            source_id=source_id,
            title=job.get("position", ""),
            location=job.get("location", ""),
            job_url=job.get("url", ""),
            description=job.get("description", "")
        )


        inserted += 1

    print(f"Offres traitées : {inserted}")


if __name__ == "__main__":
    main()