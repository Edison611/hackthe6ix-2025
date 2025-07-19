from fastapi import APIRouter
from services.ribbon import get_interviews

router = APIRouter()    

@router.get("/get_interviews")
async def get_interviews_route():
    response = await get_interviews()
    return response