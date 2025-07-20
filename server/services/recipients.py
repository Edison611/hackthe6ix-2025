from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

recipients_collection = db["recipients"]

def add_recipient(email: str, name: str):
    if recipients_collection.find_one({"email": email}):
        return {"success": False, "message": "Recipient with this email already exists."}

    recipients_collection.insert_one({
        "email": email,
        "role_ids": [],
        "name": name,
    })
    return {"success": True, "message": "Recipient added successfully."}

def update_recipient_roles(email: str, role_ids: list[str]):
    recipient = recipients_collection.find_one({"email": email})
    if not recipient:
        return {"success": False, "message": "Recipient not found."}
    
    try:
        role_object_ids = [ObjectId(rid) for rid in role_ids]
    except Exception:
        return {"success": False, "message": "Invalid role ID(s) provided."}
    
    result = recipients_collection.update_one(
        {"email": email},
        {"$set": {"role_ids": role_object_ids}}
    )
    if result.modified_count == 0:
        return {"success": False, "message": "Roles were not updated."}
    
    return {"success": True, "message": "Roles updated successfully."}

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
