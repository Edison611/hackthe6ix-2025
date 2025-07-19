# roles.py (updated to use integer role_id)
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

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
    if result.deleted_count == 0:
        return {"success": False, "message": "Role not found."}
    return {"success": True, "message": "Role deleted successfully."}
