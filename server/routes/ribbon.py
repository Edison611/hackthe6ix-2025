from fastapi import APIRouter
from services.ribbon import *

router = APIRouter()    

@router.get("/interviews")
async def get_interviews_route(interview_flow_id: str = None):
    response = await get_interviews(interview_flow_id)
    return response


@router.post("/interviews")
async def create_interview_route(title: str, questions: list[str]):
    response = await create_interview(title, questions)
    return response


@router.post("/interviews/{id}/send")
async def send_interviews_route(id: str, recipients: list[str]):
    response = await send_interviews(id, recipients)
    return response

