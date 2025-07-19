from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

recipients_collection = db["recipients"]

def add_recipient(email: str, role_ids: list[str]):
    """Add a recipient with email and list of role ObjectId strings."""
    if recipients_collection.find_one({"email": email}):
        return {"success": False, "message": "Recipient with this email already exists."}

    try:
        role_object_ids = [ObjectId(rid) for rid in role_ids]
    except Exception:
        return {"success": False, "message": "Invalid role ID(s) provided."}

    recipients_collection.insert_one({
        "email": email,
        "role_ids": role_object_ids
    })
    return {"success": True, "message": "Recipient added successfully."}

def get_recipient_by_email(email: str):
    recipient = recipients_collection.find_one({"email": email})
    if not recipient:
        return {"success": False, "message": "Recipient not found."}

    recipient["_id"] = str(recipient["_id"])
    recipient["role_ids"] = [str(rid) for rid in recipient.get("role_ids", [])]
    return recipient

def get_all_recipients():
    recipients = list(recipients_collection.find({}))
    for rec in recipients:
        rec["_id"] = str(rec["_id"])
        rec["role_ids"] = [str(rid) for rid in rec.get("role_ids", [])]
    return recipients

def delete_recipient(email: str):
    result = recipients_collection.delete_one({"email": email})
    if result.deleted_count == 0:
        return {"success": False, "message": "Recipient not found."}
    return {"success": True, "message": "Recipient deleted successfully."}
