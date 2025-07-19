from pymongo import MongoClient
from dotenv import load_dotenv
import os
import uuid  # to generate unique string IDs

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

questions_collection = db["questions"]
recipients_collection = db["recipients"]

def add_question(questions: list[str], flow_id: str, creator_email: str):
    """Add a question document with a unique string question_id and empty summary."""
    if not recipients_collection.find_one({"email": creator_email}):
        return {"success": False, "message": "Creator (recipient) not found."}

    question_id = str(uuid.uuid4())  # generate a unique string ID

    doc = {
        "question_id": question_id,
        "questions": questions,
        "flow_id": flow_id,
        "creator_email": creator_email,
        "summary": ""
    }

    result = questions_collection.insert_one(doc)
    return {"success": True, "message": "Question added successfully.", "question_id": question_id, "id": str(result.inserted_id)}

def update_summary(question_id: str, summary: str):
    """Update the summary field of a question document by question_id."""
    result = questions_collection.update_one(
        {"question_id": question_id},
        {"$set": {"summary": summary}}
    )
    if result.matched_count == 0:
        return {"success": False, "message": "Question not found."}
    return {"success": True, "message": "Summary updated successfully."}

from recipients import recipients  # your recipients collection
from responses import responses    # your responses collection

def get_response_status_for_question(question_id: str):
    # Find all recipient emails
    all_recipients = set(rec["email"] for rec in recipients.find())

    # Find recipients who responded to this question
    responded = set(resp["user_email"] for resp in responses.find({"question_id": question_id}))

    not_responded = all_recipients - responded

    return {
        "responded": list(responded),
        "not_responded": list(not_responded)
    }
