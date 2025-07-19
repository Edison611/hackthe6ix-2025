from fastapi import APIRouter
from services.ribbon import *
from services.questions import add_question
from pydantic import BaseModel
from typing import List

class InterviewCreateRequest(BaseModel):
    title: str
    questions: List[str]

router = APIRouter()    

@router.get("/responses")
async def get_interviews_route(interview_flow_id: str = None):
    response = get_interviews(interview_flow_id)
    return response


@router.get("/responses/{id}")
async def get_interviews_byId_route(id: str, recipients: list[str]):
    response = get_interviews(id, recipients)
    return response

