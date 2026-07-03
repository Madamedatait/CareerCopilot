import requests

url = "https://boards-api.greenhouse.io/v1/boards/stripe/jobs"

response = requests.get(url)

print(response.status_code)

data = response.json()

print(len(data["jobs"]))

import json

print(json.dumps(data["jobs"][0], indent=2))