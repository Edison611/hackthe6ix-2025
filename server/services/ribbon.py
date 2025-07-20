import httpx
import os
from config import RIBBON_API_KEY
from services.responses import *

# print(RIBBON_API_KEY)
BASE_URL = "https://app.ribbon.ai/be-api/v1"

# url = "https://app.ribbon.ai/be-api/v1/interview-flows"
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {RIBBON_API_KEY}",
    "content-type": "application/json"
}
# sample_data = {
#     "org_name": "ProgressLoop",
#     "title": "Standup",
#     "questions": [
#         "How's the progress on the feature you've been working on?",
#         "What are you planning to work on next?",
#         "Any problems or blockers you're facing?",
#     ]
# }

async def create_interview(title: str, questions: str):
    payload = {
        "org_name": "ProgressLoop",
        "title": title,
        "questions": questions,
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/interview-flows", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    
    
async def send_interviews(interview_flow_id: str, question_id: str, recipients: list[str]):
    payload = {
        "interview_flow_id": interview_flow_id,
    }

    ret_res = []

    for recipient in recipients:
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{BASE_URL}/interviews", headers=headers, json=payload)
            print(res.json())
            print(recipient)
            res.raise_for_status()
            ret_res.append(res.json())
            
            res2 = await add_response_async(user_email=recipient, question_id=question_id, interview_url=res.json().get("interview_link"))
            print(res2)
                    # transcript=res.json().get("transcript")
                
            # Create request to database to store the interview link

    return ret_res
            

async def get_interviews(interview_flow_id: str = None):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/interviews", headers={"Authorization": f"Bearer {RIBBON_API_KEY}"})
        res.raise_for_status()
        res = res.json()
        if interview_flow_id:
            res = [interview for interview in res if interview['interview_flow_id'] == interview_flow_id]
        return res