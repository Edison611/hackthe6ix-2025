# responses.py
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

responses = db["responses"]
recipients = db["recipients"]
questions = db["questions"]

def add_response(user_email: str, question_id: str, transcript: str, interview_url: str):
    """Add a response linked to a recipient and a question, with empty summary."""
    if not recipients.find_one({"email": user_email}):
        return {"success": False, "message": "Recipient (user) not found."}

    question_doc = questions.find_one({"question_id": question_id})
    if not question_doc:
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
responses_collection = db["responses"]
recipients_collection = db["recipients"]
questions_collection = db["questions"]

def add_response(user_email: str, question_id: str, transcript: str, interview_url: str):
    # Check user exists
    if not recipients_collection.find_one({"email": user_email}):
        return {"success": False, "message": "Recipient (user) not found."}
    # Check question exists
    if not questions_collection.find_one({"question_id": question_id}):
>>>>>>> Stashed changes
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
    try:
        oid = ObjectId(response_id)
    except Exception:
        return {"success": False, "message": "Invalid response ID."}
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

    result = responses.update_one(
        {"_id": r_oid},
        {"$set": {"summary": summary}}
    )
=======
    result = responses_collection.update_one({"_id": oid}, {"$set": {"summary": summary}})
>>>>>>> Stashed changes
=======
    result = responses_collection.update_one({"_id": oid}, {"$set": {"summary": summary}})
>>>>>>> Stashed changes
=======
    result = responses_collection.update_one({"_id": oid}, {"$set": {"summary": summary}})
>>>>>>> Stashed changes
    if result.matched_count == 0:
        return {"success": False, "message": "Response not found."}
    return {"success": True, "message": "Summary updated successfully."}


def delete_response(response_id: str):
    try:
        oid = ObjectId(response_id)
    except Exception:
        return {"success": False, "message": "Invalid response ID."}
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

    result = responses.delete_one({"_id": r_oid})
    if result.deleted_count == 0:
        return {"success": False, "message": "Response not found."}
    return {"success": True, "message": "Response deleted successfully."}
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    result = responses_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return {"success": False, "message": "Response not found."}
    return {"success": True, "message": "Response deleted successfully."}

def get_response_by_question_and_user(question_id: str, user_email: str):
    response = responses_collection.find_one({"question_id": question_id, "user_email": user_email}, {"_id": 0})
    if not response:
        return {"success": False, "message": "Response not found for given question and user."}
    return response

def get_responses_by_question_id(question_id: str):
    responses = list(responses_collection.find({"question_id": question_id}, {"_id": 0}))
    return responses

def get_all_responses():
    return list(responses_collection.find({}, {"_id": 0}))

def get_response_by_id(response_id: str):
    try:
        oid = ObjectId(response_id)
    except Exception:
        return {"success": False, "message": "Invalid response ID."}
    response = responses_collection.find_one({"_id": oid}, {"_id": 0})
    if not response:
        return {"success": False, "message": "Response not found."}
    return response
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
