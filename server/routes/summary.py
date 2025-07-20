from fastapi import APIRouter
from services.summary import summarize_response_by_id, summarize_responses_by_question_id

router = APIRouter()

@router.post("/summary/response/{response_id}")
async def summarize_single_response(response_id: str):
    return summarize_response_by_id(response_id)

@router.post("/summary/question/{question_id}")
async def summarize_all_responses_for_question(question_id: str):
    return summarize_responses_by_question_id(question_id)
