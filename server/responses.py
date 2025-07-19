# responses.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

responses = db["responses"]
recipients = db["recipients"]
questions = db["questions"]

def add_response(user_email: str, question_id: str, transcript: str, interview_url: str):
    """Add a response linked to a recipient and a question, with empty summary."""
    if not recipients.find_one({"email": user_email}):
        return {"success": False, "message": "Recipient (user) not found."}

    question_doc = questions.find_one({"question_id": question_id})
    if not question_doc:
        return {"success": False, "message": "Question not found."}

    response_doc = {
        "user_email": user_email,
        "question_id": question_id,
        "transcript": transcript,
        "interview_url": interview_url,
        "summary": ""  # starts empty
    }

    result = responses.insert_one(response_doc)
    return {"success": True, "message": "Response added successfully.", "id": str(result.inserted_id)}


def update_response_summary(response_id: str, summary: str):
    """Update the summary of a response by its ObjectId string."""
    try:
        r_oid = ObjectId(response_id)
    except Exception:
        return {"success": False, "message": "Invalid response ID."}

    result = responses.update_one(
        {"_id": r_oid},
        {"$set": {"summary": summary}}
    )
    if result.matched_count == 0:
        return {"success": False, "message": "Response not found."}
    return {"success": True, "message": "Summary updated successfully."}


def delete_response(response_id: str):
    """Delete a response by its ObjectId string."""
    try:
        r_oid = ObjectId(response_id)
    except Exception:
        return {"success": False, "message": "Invalid response ID."}

    result = responses.delete_one({"_id": r_oid})
    if result.deleted_count == 0:
        return {"success": False, "message": "Response not found."}
    return {"success": True, "message": "Response deleted successfully."}
