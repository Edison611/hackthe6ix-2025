from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

roles_collection = db["roles"]

def add_role(name: str):
    """Add a role with just a name. MongoDB _id (ObjectId) is used as the unique identifier."""
    if roles_collection.find_one({"name": name}):
        return {"success": False, "message": "Role with this name already exists."}
    result = roles_collection.insert_one({"name": name})
    return {
        "success": True,
        "message": "Role added successfully.",
        "role_id": str(result.inserted_id)
    }

def get_role_by_id(role_id: str):
    try:
        role = roles_collection.find_one({"_id": ObjectId(role_id)}, {"_id": 1, "name": 1})
    except:
        return {"success": False, "message": "Invalid role ID format."}
    
    if not role:
        return {"success": False, "message": "Role not found."}
    
    role["_id"] = str(role["_id"])
    return role

def get_all_roles():
    roles = list(roles_collection.find({}, {"_id": 1, "name": 1}))
    for role in roles:
        role["id"] = str(role["_id"])
        del role["_id"]
    return roles


def delete_role(role_id: str):
    try:
        result = roles_collection.delete_one({"_id": ObjectId(role_id)})
    except:
        return {"success": False, "message": "Invalid role ID format."}

    if result.deleted_count == 0:
        return {"success": False, "message": "Role not found."}
    return {"success": True, "message": "Role deleted successfully."}
