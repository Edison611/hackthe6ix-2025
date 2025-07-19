import httpx
import os
from config import RIBBON_API_KEY

# print(RIBBON_API_KEY)
BASE_URL = "https://app.ribbon.ai/be-api/v1"

# url = "https://app.ribbon.ai/be-api/v1/interview-flows"
# headers = {
#     "accept": "application/json",
#     "authorization": f"Bearer {RIBBON_API_KEY}",
#     "content-type": "application/json"
# }
# data = {
#     "org_name": "ProgressLoop",
#     "title": "Standup",
#     "questions": [
#         "How's the progress on the feature you've been working on?",
#         "What are you planning to work on next?",
#         "Any problems or blockers you're facing?",
#     ]
# }

# response = requests.post(url, json=data, headers=headers)

# print(response.status_code)
# print(response.json())

# async def create_interview_flow(title: str, questions: str, participants: list[str] = []):
#     payload = {
#         "title": title,
#         "questions": questions,
#         # "participants": participants  # optional if just 1 user
#     }

#     async with httpx.AsyncClient() as client:
#         res = await client.post(f"{BASE_URL}/interviews", headers=headers, json=payload)
#         res.raise_for_status()
#         return res.json()

async def get_interviews():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/interviews", headers={"Authorization": f"Bearer {RIBBON_API_KEY}"})
        res.raise_for_status()
        return res.json()