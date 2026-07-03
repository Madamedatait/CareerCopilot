import requests

from backend.services.job_filter import is_relevant_job

url = "https://remoteok.com/api"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

jobs = response.json()

relevant_jobs = []

for job in jobs[1:]:
    if is_relevant_job(job):
        relevant_jobs.append(job)

print(f"Total annonces : {len(jobs)-1}")
print(f"Annonces pertinentes : {len(relevant_jobs)}")

for job in relevant_jobs[:10]:
    print("=" * 50)
    print("COMPANY :", job.get("company"))
    print("POSITION:", job.get("position"))
    print("LOCATION:", job.get("location"))
    print("TAGS    :", job.get("tags"))