from pymongo import MongoClient
from dotenv import load_dotenv
from services.recipients import get_all_recipients
from services.responses import get_responses_by_question_id
from bson import ObjectId
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

questions_collection = db["questions"]
recipients_collection = db["recipients"]

def add_question(title: str, questions: list[str], flow_id: str, creator_email: str, roles: list[str]):
    """Add a question using MongoDB _id as primary identifier."""
    if not recipients_collection.find_one({"email": creator_email}):
        return {"success": False, "message": "Creator (recipient) not found."}

    try:
        role_object_ids = [ObjectId(rid) for rid in roles]
    except Exception:
        return {"success": False, "message": "Invalid role ID(s) provided."}

    doc = {
        "title": title,
        "questions": questions,
        "flow_id": flow_id,
        "creator_email": creator_email,
        "summary": "",
        "roles": role_object_ids
    }

    result = questions_collection.insert_one(doc)
    return {
        "success": True,
        "message": "Question added successfully.",
        "id": str(result.inserted_id)
    }

def update_summary(question_id: str, summary: str):
    """Update the summary field by MongoDB _id."""
    try:
        _id = ObjectId(question_id)
    except Exception:
        return {"success": False, "message": "Invalid question ID."}

    result = questions_collection.update_one(
        {"_id": _id},
        {"$set": {"summary": summary}}
    )
    if result.matched_count == 0:
        return {"success": False, "message": "Question not found."}
    return {"success": True, "message": "Summary updated successfully."}

def get_question_by_id(question_id: str):
    try:
        _id = ObjectId(question_id)
    except Exception:
        return {"success": False, "message": "Invalid question ID."}

    question = questions_collection.find_one({"_id": _id})
    if not question:
        return {"success": False, "message": "Question not found."}
    
    question["_id"] = str(question["_id"])
    question["roles"] = [str(rid) for rid in question.get("roles", [])]
    return question

def get_response_status_for_question(question_id: str):
    question = get_question_by_id(question_id)
    if not question or question.get("success") == False:
        return {"success": False, "message": "Question not found."}

    question_roles = set(question.get("roles", []))
    all_recipients = get_all_recipients()

    if not question_roles:
        filtered_recipients = all_recipients
    else:
        filtered_recipients = [
            rec for rec in all_recipients
            if "role_ids" in rec and question_roles.intersection(set(rec["role_ids"]))
        ]

    all_recipient_emails = set(rec["email"] for rec in filtered_recipients)
    responses_for_question = get_responses_by_question_id(question_id)
    responded = set(resp["user_email"] for resp in responses_for_question)
    not_responded = all_recipient_emails - responded

    return {
        "responded": list(responded),
        "not_responded": list(not_responded)
    }

def get_all_questions():
    questions = list(questions_collection.find({}))
    for q in questions:
        q["_id"] = str(q["_id"])
        q["roles"] = [str(rid) for rid in q.get("roles", [])]
    return questions

def get_questions_by_creator(user_email: str):
    """Get list of questions created by a specific user email."""
    print("Getting questions for user:", user_email)
    if not user_email:
        return []

    questions = list(questions_collection.find(
        {"creator_email": user_email}
    ))

    for q in questions:
        print(q)
        q["_id"] = str(q["_id"])
        q["roles"] = [str(rid) for rid in q.get("roles", [])]
    return questions
