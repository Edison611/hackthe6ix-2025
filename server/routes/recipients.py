from fastapi import APIRouter
from services.recipients import *

router = APIRouter()    

@router.get("/users")
async def get_users_route():
    response = get_all_recipients()
    return response


@router.post("/users")
async def create_users_route(email: str, name: str):
    response = add_recipient(email=email, name=name)
    return response

@router.get("/users/{id}")
async def get_interviews_route(id: str):
    return {}
# TODO get all interviews for a user

@router.put("/users/{id}")
async def update_user_role_route(id: str, role_ids: list[str]):
    response = update_recipient_roles(id, role_ids)
    return response