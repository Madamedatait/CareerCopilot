import requests

from backend.repositories.company_repository import (
    get_or_create_company
)

from backend.repositories.job_repository import (
    create_job
)

from backend.repositories.source_repository import (
    get_source_id
)


def fetch_jobs():

    url = "https://remotive.com/api/remote-jobs"

    response = requests.get(url)

    if response.status_code != 200:

        print("❌ Remotive API error")

        return []

    data = response.json()

    return data.get("jobs", [])


def main():

    source_id = get_source_id(
        "Remotive"
    )

    jobs = fetch_jobs()

    total = len(jobs)
    inserted = 0

    for job in jobs:

        company_name = job.get(
            "company_name",
            "Unknown"
        )

        company_id = get_or_create_company(
            company_name
        )

        create_job(
            company_id=company_id,
            source_id=source_id,
            title=job.get("title", ""),
            location=job.get(
                "candidate_required_location",
                ""
            ),
            job_url=job.get(
                "url",
                ""
            ),
            description=job.get(
                "description",
                ""
            )
        )

        inserted += 1

    print()
    print("===================================")
    print(f"Total jobs      : {total}")
    print(f"Inserted jobs   : {inserted}")
    print("===================================")


if __name__ == "__main__":
    main()