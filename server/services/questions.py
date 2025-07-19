from pymongo import MongoClient
from dotenv import load_dotenv
from services.recipients import get_all_recipients
from services.responses import get_responses_by_question_id
from bson import ObjectId
import os
import google.generativeai as genai
import uuid  # to generate unique string IDs

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

  
def summarize_question_responses(question_id: str):
    """Summarize all responses for a given question using Gemini API."""
    responses_result = get_responses_by_question_id(question_id) # Assuming get_responses_by_question_id also returns a dict with 'success' and 'data'
    
    # Adjust based on whether get_responses_by_question_id returns raw list or a dict
    if not responses_result or not responses_result['success'] or not responses_result['data']:
         return {"success": False, "message": "No responses found for this question."}
    
    responses = responses_result['data'] if 'data' in responses_result else responses_result # Adjust if it returns a raw list

    # Prepare the input for the Gemini API
    # Ensure there's enough content to summarize
    if not responses:
        return {"success": False, "message": "No responses found for this question."}

    # Filter out empty or invalid transcripts if necessary
    response_texts = [resp["transcript"] for resp in responses if resp.get("transcript") and resp["transcript"].strip()]
    
    if not response_texts:
        return {"success": False, "message": "No valid transcripts found to summarize."}

    # Better prompt for summarizing multiple responses
    prompt = "Please provide a concise summary of the following interview responses:\n\n" + "\n\n--- Transcript ---\n\n".join(response_texts)

    try:
        # Ensure API is configured (best done once globally)
        # genai.configure(api_key=os.getenv("GEMINI_API")) # If not configured globally already

        # Instantiate the model within the function if it's not global, or use the global one
        model = genai.GenerativeModel('gemini-1.5-flash') # Or 'gemini-pro', 'gemini-2.5-flash' if you want a specific one

        # Use generate_content for Gemini models
        gemini_response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500, # A bit more tokens for a summary of multiple responses
                temperature=0.5 # Control creativity
            )
        )

        summary = gemini_response.text.strip()
        
        if not summary:
            return {"success": False, "message": "Gemini API generated an empty summary."}

        return {"success": True, "summary": summary}
    except genai.types.BlockedPromptException as e:
        return {"success": False, "message": f"Content blocked by safety settings: {e.response.prompt_feedback.block_reason.name if e.response.prompt_feedback else 'unknown'}"}
    except genai.types.BlockedGenerationException as e:
        return {"success": False, "message": f"Generated content blocked by safety settings: {e.response.prompt_feedback.block_reason.name if e.response.prompt_feedback else 'unknown'}"}
    except Exception as e:
        # Log the full exception for debugging in a real application
        # logging.error(f"Error summarizing responses for question {question_id}: {e}", exc_info=True)
        return {"success": False, "message": f"An unexpected error occurred during summarization: {str(e)}"}



