# recipients.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

recipients = db["recipients"]

def add_recipient(email: str, role_ids: list[int]):
    """Add a new recipient with an email and list of numeric role IDs."""
    if recipients.find_one({"email": email}):
        return {"success": False, "message": "Recipient with this email already exists."}

    recipients.insert_one({
        "email": email,
        "role_ids": role_ids
    })
    return {"success": True, "message": "Recipient added successfully."}


def delete_recipient(email: str):
    """Delete a recipient by email."""
    result = recipients.delete_one({"email": email})
    if result.deleted_count == 0:
        return {"success": False, "message": "Recipient not found."}
    return {"success": True, "message": "Recipient deleted successfully."}
