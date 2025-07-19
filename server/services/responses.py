from pymongo import MongoClient
from dotenv import load_dotenv
import os
import google.generativeai as genai
from bson import ObjectId

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

responses_collection = db["responses"]
recipients_collection = db["recipients"]
questions_collection = db["questions"]

def add_response(user_email: str, question_id: str, transcript: str, interview_url: str):
    """Add a response linked to a recipient and a question, with empty summary."""
    if not recipients_collection.find_one({"email": user_email}):
        return {"success": False, "message": "Recipient (user) not found."}

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        return {"success": False, "message": "Invalid question ID."}

    if not questions_collection.find_one({"_id": q_oid}):
        return {"success": False, "message": "Question not found."}

    response_doc = {
        "user_email": user_email,
        "question_id": q_oid,
        "transcript": transcript,
        "interview_url": interview_url,
        "summary": ""
    }

    result = responses_collection.insert_one(response_doc)
    return {"success": True, "message": "Response added successfully.", "id": str(result.inserted_id)}

def update_response_summary(response_id: str, summary: str):
    """Update the summary of a response by its ObjectId string."""
    try:
        r_oid = ObjectId(response_id)
    except Exception:
        return {"success": False, "message": "Invalid response ID."}

    result = responses_collection.update_one(
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

    result = responses_collection.delete_one({"_id": r_oid})
    if result.deleted_count == 0:
        return {"success": False, "message": "Response not found."}
    return {"success": True, "message": "Response deleted successfully."}

def get_response_by_question_and_user(question_id: str, user_email: str):
    """Get a single response document by question ID and recipient email."""
    try:
        q_oid = ObjectId(question_id)
    except Exception:
        return {"success": False, "message": "Invalid question ID."}

    response = responses_collection.find_one(
        {"question_id": q_oid, "user_email": user_email},
        {"_id": 0}
    )
    if not response:
        return {"success": False, "message": "Response not found for given question and user."}
    return response

def get_responses_by_question_id(question_id: str):
    """Get list of response documents by question ID."""
    try:
        q_oid = ObjectId(question_id)
    except Exception:
        return []

    return list(responses_collection.find({"question_id": q_oid}, {"_id": 0}))

def get_response_by_id(response_id: str):
    """Get a response document by its ObjectId string."""
    try:
        r_oid = ObjectId(response_id)
    except Exception:
        return {"success": False, "message": "Invalid response ID."}

    response = responses_collection.find_one({"_id": r_oid}, {"_id": 0})
    if not response:
        return {"success": False, "message": "Response not found."}
    return response

def get_all_responses():
    """Get list of all response documents."""
    return list(responses_collection.find({}, {"_id": 0}))

def summarize_response(question_id: str, user_email: str):
    """Generate a summary for a response using Gemini API. Only summarize information from the user, not from the agent."""
    response = get_response_by_question_and_user(question_id, user_email)
    if not response:
        return {"success": False, "message": "Response not found."}

    try:
        genai.configure(api_key=os.getenv("GEMINI_API"))
        model = genai.Model("gemini-1.5-flash")
        summary = model.generate_text(
            prompt=f"Summarize the following response: {response['transcript']}",
            max_output_tokens=100
        ).text

        update_response_summary(response["_id"], summary)
        return {"success": True, "summary": summary}
    except Exception as e:
        return {"success": False, "message": str(e)}

