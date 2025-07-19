# roles.py (updated to use integer role_id)
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
<<<<<<< Updated upstream

roles = db["roles"]

def add_role(role_id: int, name: str):
    """Add a role with a given numeric ID and name."""
    if roles.find_one({"_id": role_id}):
        return {"success": False, "message": "Role with this ID already exists."}

    roles.insert_one({
        "_id": role_id,
        "name": name
    })
    return {"success": True, "message": "Role added successfully."}


def delete_role(role_id: int):
    """Delete a role by numeric ID."""
    result = roles.delete_one({"_id": role_id})
=======
roles_collection = db["roles"]

def add_role(name: str):
    """Add a role with a generated ObjectId and name."""
    result = roles_collection.insert_one({"name": name})
    return {"success": True, "message": "Role added successfully.", "id": str(result.inserted_id)}

def delete_role(role_id: str):
    """Delete a role by its ObjectId string."""
    try:
        oid = ObjectId(role_id)
    except Exception:
        return {"success": False, "message": "Invalid role ID."}
    result = roles_collection.delete_one({"_id": oid})
>>>>>>> Stashed changes
    if result.deleted_count == 0:
        return {"success": False, "message": "Role not found."}
    return {"success": True, "message": "Role deleted successfully."}

def get_role_by_id(role_id: str):
    try:
        oid = ObjectId(role_id)
    except Exception:
        return {"success": False, "message": "Invalid role ID."}
    role = roles_collection.find_one({"_id": oid}, {"_id": 0})
    if not role:
        return {"success": False, "message": "Role not found."}
    return role

def get_all_roles():
    roles = list(roles_collection.find({}, {"_id": 0}))
    return roles
