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


def summarize_response_by_id(response_id: str):
    """
    Summarizes the transcript of a single response using Gemini 2.5,
    and updates its 'summary' field *only if it's currently empty*.
    """
    try:
        response_doc = responses.find_one({"_id": ObjectId(response_id)})

        if not response_doc:
            return {"success": False, "message": "Response not found."}

        existing_summary = response_doc.get("summary", "")
        if isinstance(existing_summary, str) and existing_summary.strip():
            return {"success": True, "skipped": True, "message": "Already summarized. Skipping."}

        transcript = response_doc.get("transcript", "")
        if not transcript or not isinstance(transcript, str):
            return {"success": False, "message": "Transcript is empty or invalid."}

        prompt = (
            "The following is a transcript of an interview between a user and an interviewer.\n"
            "Only summarize what the user said. Ignore the agent/interviewer.\n\n"
            f"{transcript}"
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        result = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.5
            )
        )

        if not hasattr(result, "parts") or not result.parts:
            return {"success": False, "message": "Gemini returned no usable content."}

        summary = ''.join(
            part.text for part in result.parts if hasattr(part, "text")
        ).strip()

        if not summary:
            return {"success": False, "message": "Gemini returned an empty summary."}

        update_result = responses.update_one(
            {"_id": ObjectId(response_id)},
            {"$set": {"summary": summary}}
        )

        if update_result.modified_count == 0:
            return {"success": False, "message": "Summary generated but DB update failed."}

        return {"success": True, "summary": summary}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def summarize_responses_by_question_id(question_id: str):
    """
    Summarizes all non-empty response summaries linked to a question ID,
    and updates the 'summary' field of that question using Gemini 1.5 Pro.
    """
    try:
        response_docs = list(responses.find({"question_id": ObjectId(question_id)}))

        if not response_docs:
            return {"success": False, "message": "No responses found for this question."}

        response_summaries = [
            r["summary"] for r in response_docs
            if r.get("summary") and isinstance(r["summary"], str) and r["summary"].strip()
        ]

        if not response_summaries:
            return {"success": False, "message": "No valid response summaries found."}

        prompt = (
            "Summarize the following user feedback into 3–5 sentences. "
            "Identify key themes, concerns, and opinions. Don't list individual responses.\n\n"
            + "\n\n--- Response Summary ---\n\n".join(response_summaries)
        )

        model = genai.GenerativeModel("gemini-1.5-pro")
        result = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.5
            )
        )

        if not hasattr(result, "parts") or not result.parts:
            return {"success": False, "message": "Gemini returned no usable content."}

        final_summary = ''.join(
            part.text for part in result.parts if hasattr(part, "text")
        ).strip()

        if not final_summary:
            return {"success": False, "message": "Gemini returned an empty summary."}

        update_result = questions.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": {"summary": final_summary}}
        )

        if update_result.modified_count == 0:
            return {"success": False, "message": "Summary generation succeeded, but DB update failed."}

        return {"success": True, "summary": final_summary}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
