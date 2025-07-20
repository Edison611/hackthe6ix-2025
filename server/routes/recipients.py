from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from services.recipients import *

router = APIRouter()

class RoleUpdateRequest(BaseModel):
    role_ids: list[str]

@router.get("/users")
async def get_users_route():
    return get_all_recipients()

@router.post("/users")
async def create_users_route(email: str, name: str):
    return add_recipient(email=email, name=name)

@router.get("/users/{id}")
async def get_interviews_route(id: str):
    return {}  # TODO

@router.put("/users/{email}")
async def update_user_role_route(email: str, body: RoleUpdateRequest = Body(...)):
    response = update_recipient_roles(email, body.role_ids)
    if not response.get("success", False):
        raise HTTPException(status_code=400, detail=response.get("message", "Failed to update roles"))
    return response
