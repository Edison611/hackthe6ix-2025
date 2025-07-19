from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import google.generativeai as genai

# === Setup ===
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
questions = db["questions"]
responses = db["responses"]

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API"))

def summarize_responses_by_question_id(question_id: str):
    """
    Summarizes all response summaries linked to a question ID,
    and updates the 'summary' field of that question.
    """
    try:
        # Fetch all responses related to this question
        response_docs = list(responses.find({"question_id": ObjectId(question_id)}))

        if not response_docs:
            return {"success": False, "message": "No responses found for this question."}

        # Get summaries from responses
        response_summaries = [
            r["summary"] for r in response_docs
            if r.get("summary") and isinstance(r["summary"], str) and r["summary"].strip()
        ]

        if not response_summaries:
            return {"success": False, "message": "No valid response summaries found."}

        # Build prompt for Gemini
        prompt = (
            "Please generate a concise summary based on these individual response summaries:\n\n"
            + "\n\n--- Response Summary ---\n\n".join(response_summaries)
        )

        # Use Gemini to generate a combined summary
        model = genai.GenerativeModel("gemini-1.5-flash")
        result = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500,
                temperature=0.5
            )
        )
        final_summary = result.text.strip()

        if not final_summary:
            return {"success": False, "message": "Gemini returned an empty summary."}

        # Update the question with the generated summary
        update_result = questions.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": {"summary": final_summary}}
        )

        if update_result.modified_count == 0:
            return {"success": False, "message": "Summary generation succeeded, but DB update failed."}

        return {"success": True, "summary": final_summary}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def summarize_response_by_id(response_id: str):
    """
    Summarizes the transcript of a single response (by ID) using Gemini,
    and updates its 'summary' field in the database.
    """
    try:
        # Fetch response by ObjectId
        response_doc = responses.find_one({"_id": ObjectId(response_id)})

        if not response_doc:
            return {"success": False, "message": "Response not found."}

        transcript = response_doc.get("transcript", "")
        if not transcript or not isinstance(transcript, str):
            return {"success": False, "message": "Transcript is empty or invalid."}

        # Build prompt for Gemini
        prompt = (
            "The following is a transcript of an interview between a user and an interviewer.\n"
            "Only summarize what the user said. Ignore the agent/interviewer.\n\n"
            f"{transcript}"
        )

        # Generate summary using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        result = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.5
            )
        )
        summary = result.text.strip()

        if not summary:
            return {"success": False, "message": "Gemini returned an empty summary."}

        # Update response document with summary
        update_result = responses.update_one(
            {"_id": ObjectId(response_id)},
            {"$set": {"summary": summary}}
        )

        if update_result.modified_count == 0:
            return {"success": False, "message": "Summary generation succeeded, but DB update failed."}

        return {"success": True, "summary": summary}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}