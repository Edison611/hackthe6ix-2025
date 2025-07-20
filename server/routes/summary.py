from fastapi import APIRouter
from services.summary import summarize_response_by_id, summarize_responses_by_question_id
from services.responses import *
from services.ribbon import *


router = APIRouter()

@router.get("/summary/response/{response_id}")
async def summarize_single_response(response_id: str):
    res = get_response(response_id)
    print(res)
    response = await get_interview_by_id(res.get("interview_id"))
    # print(response)
    print(response["interview_data"]["transcript"])

    return summarize_response_by_id(response_id, transcript=response["interview_data"].get("transcript"))


@router.get("/summary/question/{question_id}")
async def summarize_all_responses_for_question(interview_id: str, question_id: str):
    return summarize_responses_by_question_id(question_id)
