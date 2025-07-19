from fastapi import APIRouter
from services.questions import *

router = APIRouter()    

@router.get("/questions")
async def get_questions_route():
    response = get_all_questions()
    return response

@router.post("/questions/summarize")
async def summarize_q_responses(question_id: str):
    response = summarize_question_responses(question_id)
    return response

@router.get("/questions/{id}")
async def get_q_by_id(id: str):
    response = get_question_by_id(id)
    return response