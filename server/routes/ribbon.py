from fastapi import APIRouter
from services.ribbon import *
from services.questions import add_question
from pydantic import BaseModel
from typing import List
from  services.recipients import get_all_recipients

class InterviewCreateRequest(BaseModel):
    title: str
    questions: List[str]
    creator_email: str
    roles: List[str]

router = APIRouter()    

@router.get("/interviews")
async def get_interviews_route(interview_flow_id: str = None):
    response = await get_interviews(interview_flow_id)
    return response


@router.post("/interviews")
async def create_interview_route(data: InterviewCreateRequest):
    print(data)
    response = await create_interview(data.title, data.questions)
    flow_id = response.get("interview_flow_id")
    print(response)
    question = add_question(title=data.title, questions=data.questions, flow_id=flow_id, creator_email=data.creator_email, roles=data.roles)
    all_recipients = get_all_recipients()
    print("All recipients:", all_recipients)
    r = []
    for recipient in all_recipients:
        for role in data.roles:
            if role in recipient.get("role_ids", []):
                r.append(recipient.get("email"))
    print(len(all_recipients))
    print(len(r))
    print(flow_id)
    await send_interviews(flow_id, question["id"], r)
    print(response)

    return response


@router.post("/interviews/{id}/send")
async def send_interviews_route(id: str, recipients: list[str]):
    response = await send_interviews(id, recipients)
    return response

