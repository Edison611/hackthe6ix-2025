from pymongo import MongoClient
from dotenv import load_dotenv
from recipients import get_all_recipients
from responses import get_responses_by_question_id
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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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

=======
    responses_result = get_responses_by_question_id(question_id)
    
    # Handle both cases: dict with success/data or a raw list
    if isinstance(responses_result, dict):
        if not responses_result.get('success', False) or not responses_result.get('data'):
            return {"success": False, "message": "No responses found for this question."}
        responses = responses_result['data']
    else:
        responses = responses_result

    if not responses:
        return {"success": False, "message": "No responses found for this question."}

=======
    responses_result = get_responses_by_question_id(question_id)
    
    # Handle both cases: dict with success/data or a raw list
    if isinstance(responses_result, dict):
        if not responses_result.get('success', False) or not responses_result.get('data'):
            return {"success": False, "message": "No responses found for this question."}
        responses = responses_result['data']
    else:
        responses = responses_result

    if not responses:
        return {"success": False, "message": "No responses found for this question."}

>>>>>>> Stashed changes
=======
    responses_result = get_responses_by_question_id(question_id)
    
    # Handle both cases: dict with success/data or a raw list
    if isinstance(responses_result, dict):
        if not responses_result.get('success', False) or not responses_result.get('data'):
            return {"success": False, "message": "No responses found for this question."}
        responses = responses_result['data']
    else:
        responses = responses_result

    if not responses:
        return {"success": False, "message": "No responses found for this question."}

>>>>>>> Stashed changes
=======
    responses_result = get_responses_by_question_id(question_id)
    
    # Handle both cases: dict with success/data or a raw list
    if isinstance(responses_result, dict):
        if not responses_result.get('success', False) or not responses_result.get('data'):
            return {"success": False, "message": "No responses found for this question."}
        responses = responses_result['data']
    else:
        responses = responses_result

    if not responses:
        return {"success": False, "message": "No responses found for this question."}

>>>>>>> Stashed changes
    # Filter out empty or invalid transcripts
    response_texts = [resp.get("transcript", "").strip() for resp in responses if resp.get("transcript") and resp["transcript"].strip()]
    if not response_texts:
        return {"success": False, "message": "No valid transcripts found to summarize."}

    prompt = (
        "Please provide a concise summary of the following interview responses:\n\n" +
        "\n\n--- Transcript ---\n\n".join(response_texts)
    )

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Adjust model name if needed
        gemini_response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500,
                temperature=0.5,
            )
        )
        summary = gemini_response.text.strip()

        if not summary:
            return {"success": False, "message": "Gemini API generated an empty summary."}

        return {"success": True, "summary": summary}
    
    except genai.types.BlockedPromptException as e:
        reason = e.response.prompt_feedback.block_reason.name if e.response.prompt_feedback else "unknown"
        return {"success": False, "message": f"Content blocked by safety settings: {reason}"}
    except genai.types.BlockedGenerationException as e:
        reason = e.response.prompt_feedback.block_reason.name if e.response.prompt_feedback else "unknown"
        return {"success": False, "message": f"Generated content blocked by safety settings: {reason}"}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred during summarization: {str(e)}"}
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
