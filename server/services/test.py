from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import pprint
from summary import summarize_responses_by_question_id

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
questions = db["questions"]
responses = db["responses"]

pp = pprint.PrettyPrinter(indent=2)

def test_summary_generation():
    # 1. Insert a fake question
    question = {
        "creator_email": "tester@example.com",
        "flow_id": "test-flow",
        "questions": ["How do you feel about our remote policy?"],
        "roles": [],
        "summary": "",
        "title": "Remote Policy Feedback"
    }
    question_id = questions.insert_one(question).inserted_id
    print(f"Created test question with ID: {question_id}")

    # 2. Insert fake responses with summaries
    response_summaries = [
        "I love working remotely; it's improved my productivity.",
        "Remote work makes collaboration harder, but I like the flexibility.",
        "The remote policy is fair, but hybrid would be better for team cohesion.",
        "No issues with the policy, just wish for clearer expectations.",
        "Remote work is convenient, but sometimes I miss in-person meetings."
    ]

    for summary in response_summaries:
        responses.insert_one({
            "question_id": question_id,
            "email": "user@example.com",
            "answers": ["Sample answer"],
            "summary": summary
        })

    # 3. Run the summarizer
    result = summarize_responses_by_question_id(str(question_id))
    print("\n=== Summarization Result ===")
    pp.pprint(result)

    # 4. Verify DB was updated
    updated_question = questions.find_one({"_id": question_id})
    print("\n=== Updated Question Summary ===")
    print(updated_question.get("summary", "(No summary)"))

if __name__ == "__main__":
    test_summary_generation()
