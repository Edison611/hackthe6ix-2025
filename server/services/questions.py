from pymongo import MongoClient
from dotenv import load_dotenv
from recipients import get_all_recipients
from responses import get_responses_by_question_id
import os
import google.generativeai as genai
import uuid  # to generate unique string IDs

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

questions_collection = db["questions"]
recipients_collection = db["recipients"]

def add_question(title: str, questions: list[str], flow_id: str, creator_email: str, roles: list):
    """Add a question document with title, unique string question_id, empty summary, and assigned roles."""
    if not recipients_collection.find_one({"email": creator_email}):
        return {"success": False, "message": "Creator (recipient) not found."}

    question_id = str(uuid.uuid4())  # generate a unique string ID

    doc = {
        "title": title,
        "question_id": question_id,
        "questions": questions,
        "flow_id": flow_id,
        "creator_email": creator_email,
        "summary": "",
        "roles": roles  # list of role IDs associated with this question
    }

    result = questions_collection.insert_one(doc)
    return {
        "success": True,
        "message": "Question added successfully.",
        "question_id": question_id,
        "id": str(result.inserted_id)
    }

def update_summary(question_id: str, summary: str):
    """Update the summary field of a question document by question_id."""
    result = questions_collection.update_one(
        {"question_id": question_id},
        {"$set": {"summary": summary}}
    )
    if result.matched_count == 0:
        return {"success": False, "message": "Question not found."}
    return {"success": True, "message": "Summary updated successfully."}

def get_question_by_id(question_id: str):
    question = questions_collection.find_one({"question_id": question_id}, {"_id": 0})
    if not question:
        return {"success": False, "message": "Question not found."}
    return question

def get_response_status_for_question(question_id: str):
    question = get_question_by_id(question_id)
    if not question or question.get("success") == False:
        return {"success": False, "message": "Question not found."}

    question_roles = set(question.get("roles", []))
    all_recipients = get_all_recipients()

    if not question_roles:
        # No roles specified - consider all recipients
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
    return list(questions_collection.find({}, {"_id": 0}))

def summarize_question_responses(question_id: str):
    """Summarize all responses for a given question using Gemini API."""
    responses = get_responses_by_question_id(question_id)
    if not responses:
        return {"success": False, "message": "No responses found for this question."}

    # Prepare the input for the Gemini API
    response_texts = [resp["transcript"] for resp in responses]
    prompt = f"Summarize the following responses:\n\n" + "\n\n".join(response_texts)

    try:
        genai.configure(api_key=os.getenv("GEMINI_API"))
        response = genai.generate_text(prompt=prompt)
        summary = response.text.strip()
        return {"success": True, "summary": summary}
    except Exception as e:
        return {"success": False, "message": str(e)}
