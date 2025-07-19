from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

roles_collection = db["roles"]

def add_role(role_id: int, name: str):
    """Add a role with a numeric role_id and name. MongoDB _id is auto-generated."""
    if roles_collection.find_one({"role_id": role_id}):
        return {"success": False, "message": "Role with this ID already exists."}
    roles_collection.insert_one({
        "role_id": role_id,
        "name": name
    })
    return {"success": True, "message": "Role added successfully."}

def get_role_by_id(role_id: int):
    role = roles_collection.find_one({"role_id": role_id}, {"_id": 1, "role_id": 1, "name": 1})
    if not role:
        return {"success": False, "message": "Role not found."}
    # Convert ObjectId to string
    role["_id"] = str(role["_id"])
    return role

def get_all_roles():
    roles = list(roles_collection.find({}, {"_id": 1, "role_id": 1, "name": 1}))
    for role in roles:
        role["_id"] = str(role["_id"])
    return roles

def delete_role(role_id: int):
    result = roles_collection.delete_one({"role_id": role_id})
    if result.deleted_count == 0:
        return {"success": False, "message": "Role not found."}
    return {"success": True, "message": "Role deleted successfully."}
