from fastapi import APIRouter
from services.questions import *
from services.summary import *


router = APIRouter()    

@router.get("/questions")
async def get_questions_route():
    response = get_all_questions()
    return response

@router.post("/questions/summarize")
async def summarize_q_responses(question_id: str):
    response = summarize_responses_by_question_id(question_id)
    return response

@router.get("/questions/{id}")
async def get_q_by_id(id: str):
    response = get_question_by_id(id)
    return response

@router.get("/questions/creator/{email}")
async def get_questions_by_creator_route(email: str):
    response = get_questions_by_creator(email)
    return response


@router.get("/questions/{id}/responses")
async def get_responses_by_question_id_route(id: str):
    response = get_responses_for_question(id)
    return response

@router.get("/questions/{id}/response-status")
async def get_response_status(id: str):
    return get_response_status_for_question(id)