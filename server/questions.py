from pymongo import MongoClient
from dotenv import load_dotenv
<<<<<<< Updated upstream
import os
from bson import ObjectId
import uuid  # to generate unique string IDs
=======
from bson import ObjectId
import uuid
import os
from responses import get_responses_by_question_id
>>>>>>> Stashed changes

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
questions_collection = db["questions"]
recipients_collection = db["recipients"]

<<<<<<< Updated upstream
def add_question(questions: list[str], flow_id: str, creator_email: str):
    """Add a question document with a unique string question_id and empty summary."""
=======
def add_question(questions, flow_id, creator_email, roles):
    """Add a question document with unique string question_id, empty summary, and list of role ObjectId strings."""
    # Validate creator exists
>>>>>>> Stashed changes
    if not recipients_collection.find_one({"email": creator_email}):
        return {"success": False, "message": "Creator (recipient) not found."}

    try:
        role_oids = [ObjectId(role) for role in roles]
    except Exception:
        return {"success": False, "message": "One or more invalid role IDs."}

    question_id = str(uuid.uuid4())
    doc = {
        "question_id": question_id,
        "questions": questions,
        "flow_id": flow_id,
        "creator_email": creator_email,
<<<<<<< Updated upstream
        "summary": ""
=======
        "summary": "",
        "roles": role_oids
>>>>>>> Stashed changes
    }

    result = questions_collection.insert_one(doc)
    return {"success": True, "message": "Question added successfully.", "question_id": question_id, "id": str(result.inserted_id)}

def update_summary(question_id: str, summary: str):
    result = questions_collection.update_one({"question_id": question_id}, {"$set": {"summary": summary}})
    if result.matched_count == 0:
        return {"success": False, "message": "Question not found."}
    return {"success": True, "message": "Summary updated successfully."}

<<<<<<< Updated upstream
from recipients import recipients  # your recipients collection
from responses import responses    # your responses collection
=======
def get_question_by_id(question_id: str):
    question = questions_collection.find_one({"question_id": question_id}, {"_id": 0})
    if not question:
        return {"success": False, "message": "Question not found."}
    # convert role ObjectIds to strings
    question["roles"] = [str(rid) for rid in question.get("roles", [])]
    return question
>>>>>>> Stashed changes

def get_all_questions():
    questions = list(questions_collection.find({}, {"_id": 0}))
    # convert role ObjectIds to strings
    for q in questions:
        q["roles"] = [str(rid) for rid in q.get("roles", [])]
    return questions

def get_response_status_for_question(question_id: str):
<<<<<<< Updated upstream
    # Find all recipient emails
    all_recipients = set(rec["email"] for rec in recipients.find())

    # Find recipients who responded to this question
    responded = set(resp["user_email"] for resp in responses.find({"question_id": question_id}))

    not_responded = all_recipients - responded

    return {
        "responded": list(responded),
        "not_responded": list(not_responded)
    }
=======
    question = get_question_by_id(question_id)
    if not question.get("success", True):
        return {"success": False, "message": "Question not found."}

    question_roles = question.get("roles", [])
    # Fetch recipients with any matching role ObjectId
    potential_recipients = list(recipients_collection.find({"role_ids": {"$in": [ObjectId(rid) for rid in question_roles]}}, {"email": 1}))
    all_emails = [r["email"] for r in potential_recipients]

    responses = get_responses_by_question_id(question_id)
    responded_emails = [resp["user_email"] for resp in responses]

    not_responded = list(set(all_emails) - set(responded_emails))
    return {"responded": responded_emails, "not_responded": not_responded}
>>>>>>> Stashed changes
