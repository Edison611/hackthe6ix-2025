from fastapi import APIRouter
from services.roles import *

router = APIRouter()    

@router.get("/roles")
async def get_roles():
    response = get_all_roles()
    return response
