from fastapi import APIRouter
from services.ribbon import *
from services.responses import *
from pydantic import BaseModel
from typing import List

class InterviewCreateRequest(BaseModel):
    title: str
    questions: List[str]

router = APIRouter()    

@router.get("/responses")
async def get_response_route(question_id: str):
    response = get_responses_by_question_id(question_id)
    return response

@router.get("/responses/{email}")
async def get_responses_assigned_to_user_route(email: str):
    response = get_responses_assigned_to_user(email)
    return response


# @router.get("/responses/{id}")
# async def get_interviews_byId_route(id: str, recipients: list[str]):
#     response = get_response_by_question_and_user(id, recipients)
#     return response


