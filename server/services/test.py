from recipients import add_recipient, update_recipient_roles
from roles import add_role
from questions import add_question, get_question_by_id
from responses import add_response
from summary import summarize_response_by_id, summarize_responses_by_question_id

# Test constants
ROLE_NAME = "Designer"
QUESTION_TITLE = "Tool Feedback"
QUESTION_FLOW_ID = "feedback-flow-1"
QUESTION_TEXT = ["What's your favorite design tool?", "Why?"]

USERS = [
    {"email": "alice@example.com", "name": "Alice", "transcript": "User: I love using Figma because it’s fast and collaborative."},
    {"email": "bob@example.com", "name": "Bob", "transcript": "User: Photoshop is my go-to tool for high-end graphics work."}
]

def test_question_summary_with_multiple_users():
    print("=== Setup Role and Recipients ===")
    role_res = add_role(ROLE_NAME)
    assert role_res["success"], role_res["message"]
    role_id = role_res["role_id"]

    for user in USERS:
        add_recipient(user["email"], user["name"])
        update_recipient_roles(user["email"], [role_id])

    print("=== Add Question ===")
    q_res = add_question(
        title=QUESTION_TITLE,
        questions=QUESTION_TEXT,
        flow_id=QUESTION_FLOW_ID,
        creator_email=USERS[0]["email"],
        roles=[role_id]
    )
    assert q_res["success"], q_res["message"]
    question_id = q_res["id"]

    print("=== Add Responses and Summarize Each ===")
    for user in USERS:
        r = add_response(user["email"], question_id, user["transcript"], "http://example.com/interview")
        assert r["success"], r["message"]
        response_id = r["id"]
        print(f"Summarizing response for {user['email']}...")
        res_summary = summarize_response_by_id(response_id)
        print(res_summary)

    print("\n=== Summarizing Entire Question ===")
    final_summary = summarize_responses_by_question_id(question_id)
    print("Final Summary:", final_summary)

    print("\n=== Updated Question Document ===")
    q = get_question_by_id(question_id)
    print("Question Summary:", q["summary"])

if __name__ == "__main__":
    test_question_summary_with_multiple_users()
