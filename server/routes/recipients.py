from fastapi import APIRouter
from services.recipients import *

router = APIRouter()    

@router.get("/users")
async def get_users_route():
    response = get_all_recipients()
    return response


@router.post("/users")
async def create_users_route(email: str):
    response = add_recipient(email=email)
    return response

@router.get("/users/{id}")
async def get_interviews_route(id: str):
    return {}

@router.put("/users/{id}")
async def update_user_route(id: str, email: str):
    # TODO: Implement update logic
    return