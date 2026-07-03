import requests

from backend.services.job_filter import is_relevant_job
from backend.repositories.company_repository import get_or_create_company
from backend.repositories.job_repository import create_job
from backend.repositories.source_repository import get_source_id

from backend.config.greenhouse_boards import GREENHOUSE_BOARDS


def fetch_jobs(board):

    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Erreur board: {board}")
        return []

    data = response.json()

    return data.get("jobs", [])


def main():

    source_id = get_source_id("Greenhouse")

    all_jobs = []

    for board in GREENHOUSE_BOARDS:

        jobs = fetch_jobs(board)

        print(f"✅ {board}: {len(jobs)} jobs")

        all_jobs.extend(jobs)

    total = len(all_jobs)
    relevant = 0
    inserted = 0

    for job in all_jobs:

        normalized_job = {
            "position": job.get("title", ""),
            "company": job.get("company_name", ""),
            "location": job.get("location", {}).get("name", ""),
            "url": job.get("absolute_url", ""),
            "description": job.get("content", "")
        }

        if not is_relevant_job(normalized_job):
            continue

        relevant += 1

        company_id = get_or_create_company(
            normalized_job["company"]
        )

        print("Description length:", len(normalized_job["description"]))
    
        create_job(
            company_id=company_id,
            source_id=source_id,
            title=normalized_job["position"],
            location=normalized_job["location"],
            job_url=normalized_job["url"],
            description=normalized_job["description"]
        )

        inserted += 1

    print()
    print("===================================")
    print(f"Total jobs      : {total}")
    print(f"Relevant jobs   : {relevant}")
    print(f"Inserted jobs   : {inserted}")
    print("===================================")


if __name__ == "__main__":
    main()