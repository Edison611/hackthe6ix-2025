import requests
from dotenv import load_dotenv
import os

load_dotenv()

RIBBON_API_KEY = os.getenv("RIBBON_API_KEY")

url = "https://app.ribbon.ai/be-api/v1/interview-flows"
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {RIBBON_API_KEY}",
    "content-type": "application/json"
}
data = {
    "org_name": "ProgressLoop",
    "title": "Standup",
    "questions": [
        "How's the progress on the feature you've been working on?",
        "What are you planning to work on next?",
        "Any problems or blockers you're facing?",
    ]
}

response = requests.post(url, json=data, headers=headers)

print(response.status_code)
print(response.json())
