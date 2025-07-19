# recipients.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
<<<<<<< Updated upstream
<<<<<<< Updated upstream

recipients = db["recipients"]

def add_recipient(email: str, role_ids: list[int]):
    """Add a new recipient with an email and list of numeric role IDs."""
    if recipients.find_one({"email": email}):
        return {"success": False, "message": "Recipient with this email already exists."}

    recipients.insert_one({
=======
recipients_collection = db["recipients"]

=======
recipients_collection = db["recipients"]

>>>>>>> Stashed changes
def add_recipient(email: str, role_ids: list[str]):
    """Add a recipient with email and list of role ObjectId strings."""
    try:
        role_oids = [ObjectId(rid) for rid in role_ids]
    except Exception:
        return {"success": False, "message": "One or more invalid role IDs."}

    if recipients_collection.find_one({"email": email}):
        return {"success": False, "message": "Recipient with this email already exists."}

    result = recipients_collection.insert_one({
<<<<<<< Updated upstream
>>>>>>> Stashed changes
        "email": email,
        "role_ids": role_oids
    })
<<<<<<< Updated upstream
    return {"success": True, "message": "Recipient added successfully."}

=======
    return {"success": True, "message": "Recipient added successfully.", "id": str(result.inserted_id)}
>>>>>>> Stashed changes
=======
        "email": email,
        "role_ids": role_oids
    })
    return {"success": True, "message": "Recipient added successfully.", "id": str(result.inserted_id)}
>>>>>>> Stashed changes

def delete_recipient(email: str):
    """Delete a recipient by email."""
    result = recipients.delete_one({"email": email})
    if result.deleted_count == 0:
        return {"success": False, "message": "Recipient not found."}
    return {"success": True, "message": "Recipient deleted successfully."}

def get_recipient_by_email(email: str):
    recipient = recipients_collection.find_one({"email": email}, {"_id": 0})
    if not recipient:
        return {"success": False, "message": "Recipient not found."}
    # convert role ObjectIds to strings for convenience
    recipient["role_ids"] = [str(rid) for rid in recipient.get("role_ids", [])]
    return recipient

def get_all_recipients():
    recipients = list(recipients_collection.find({}, {"_id": 0}))
    # convert ObjectIds in role_ids to strings
    for r in recipients:
        r["role_ids"] = [str(rid) for rid in r.get("role_ids", [])]
    return recipients
