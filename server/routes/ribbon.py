from fastapi import APIRouter
from services.ribbon import *
from services.questions import add_question
from pydantic import BaseModel
from typing import List

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
    response = await create_interview(data.title, data.questions)
    print(response)
    response = add_question(title=data.title, questions=data.questions, flow_id=response.get("interview_flow_id"), creator_email=data.creator_email, roles=data.roles)
    print(response)
    
    return response


@router.post("/interviews/{id}/send")
async def send_interviews_route(id: str, recipients: list[str]):
    response = await send_interviews(id, recipients)
    return response

