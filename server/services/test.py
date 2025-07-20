from responses import get_responses_assigned_to_user
from questions import get_questions_by_creator

def test_get_questions_by_creator():
    print("Running test_get_questions_by_creator...")

    test_email = "test_creator@example.com"
    questions = get_questions_by_creator(test_email)

    assert isinstance(questions, list), "Expected a list of questions"
    for q in questions:
        assert isinstance(q["_id"], str), "_id must be a string"
        assert q.get("creatorEmail") == test_email, "creatorEmail mismatch"

    print(f"✅ Passed: Found {len(questions)} questions for {test_email}")

def test_get_responses_assigned_to_user():
    print("Running test_get_responses_assigned_to_user...")

    test_email = "responder@example.com"
    responses = get_responses_assigned_to_user(test_email)

    assert isinstance(responses, list), "Expected a list of responses"
    for r in responses:
        assert isinstance(r["_id"], str), "_id must be a string"
        assert isinstance(r["question_id"], str), "question_id must be a string"
        assert r.get("user_email") == test_email, "user_email mismatch"

    print(f"✅ Passed: Found {len(responses)} responses assigned to {test_email}")


if __name__ == "__main__":
    test_get_questions_by_creator()
    test_get_responses_assigned_to_user()
