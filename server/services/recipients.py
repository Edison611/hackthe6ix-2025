from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

recipients_collection = db["recipients"]

def add_recipient(email: str, role_ids: list[int]):
    """Add a recipient with email and role_ids."""
    if recipients_collection.find_one({"email": email}):
        return {"success": False, "message": "Recipient with this email already exists."}
    recipients_collection.insert_one({
        "email": email,
        "role_ids": role_ids
    })
    return {"success": True, "message": "Recipient added successfully."}

def get_recipient_by_email(email: str):
    recipient = recipients_collection.find_one({"email": email}, {"_id": 1, "email": 1, "role_ids": 1})
    if not recipient:
        return {"success": False, "message": "Recipient not found."}
    recipient["_id"] = str(recipient["_id"])
    return recipient

def get_all_recipients():
    recipients = list(recipients_collection.find({}, {"_id": 1, "email": 1, "role_ids": 1}))
    for rec in recipients:
        rec["_id"] = str(rec["_id"])
    return recipients

def delete_recipient(email: str):
    result = recipients_collection.delete_one({"email": email})
    if result.deleted_count == 0:
        return {"success": False, "message": "Recipient not found."}
    return {"success": True, "message": "Recipient deleted successfully."}
