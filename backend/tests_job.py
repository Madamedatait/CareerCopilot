from backend.repositories.company_repository import get_or_create_company
from backend.repositories.job_repository import create_job

REMOTEOK_SOURCE_ID = "b60a9c8a-a253-47bf-ace0-10664dd19508"

company_id = get_or_create_company("Scalingo")

job_id = create_job(
    company_id=company_id,
    source_id=REMOTEOK_SOURCE_ID,
    title="Platform Support Engineer",
    location="Remote Europe",
    job_url="https://scalingo.com/careers/platform-support-engineer"
)

print("Job created:", job_id)