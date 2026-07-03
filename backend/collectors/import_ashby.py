import requests

from backend.services.job_filter import is_relevant_job
from backend.repositories.company_repository import get_or_create_company
from backend.repositories.job_repository import create_job
from backend.repositories.source_repository import get_source_id

from backend.config.ashby_boards import ASHBY_BOARDS


def fetch_jobs(board):

    url = f"https://api.ashbyhq.com/posting-api/job-board/{board}"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Erreur board: {board}")
        return []

    data = response.json()

    return data.get("jobs", [])


def main():

    source_id = get_source_id("Ashby")

    all_jobs = []

    for board in ASHBY_BOARDS:

        jobs = fetch_jobs(board)

        print(f"✅ {board}: {len(jobs)} jobs")

        for job in jobs:

            job["board"] = board

        all_jobs.extend(jobs)

    total = len(all_jobs)
    relevant = 0
    inserted = 0

    for job in all_jobs:

        normalized_job = {
            "position": job.get("title", ""),
            "company": job.get("board", "").capitalize(),
            "location": job.get("location", ""),
            "url": job.get("jobUrl", ""),
            "description": job.get("descriptionPlain", "")
        }

        if not is_relevant_job(normalized_job):
            continue

        relevant += 1

        company_id = get_or_create_company(
            normalized_job["company"]
        )

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