import requests

company = "notion"

url = f"https://api.ashbyhq.com/posting-api/job-board/{company}"

response = requests.get(url)

data = response.json()

print(data.keys())

print()

print("Nombre de jobs :", len(data["jobs"]))

print()

print(data["jobs"][0])