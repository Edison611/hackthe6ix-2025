from roles import add_role, get_all_roles
from recipients import add_recipient, get_all_recipients
from questions import add_question, get_all_questions, get_response_status_for_question
from responses import add_response, get_response_by_question_and_user, get_all_responses

# === Test roles ===
print("\n--- Adding Roles ---")
add_role(1, "Developer")
add_role(2, "Designer")
print(get_all_roles())

# === Test recipients ===
print("\n--- Adding Recipients ---")
add_recipient("dev@example.com", [1])
add_recipient("design@example.com", [2])
add_recipient("fullstack@example.com", [1, 2])
print(get_all_recipients())

# === Test questions ===
print("\n--- Adding Questions ---")
q_result = add_question(
    questions=["What is your development experience?"],
    flow_id="flow_123",
    creator_email="dev@example.com",
    roles=[1]
)
question_id = q_result["question_id"]
print(f"Created question: {question_id}")
print(get_all_questions())

# === Test responses ===
print("\n--- Adding Responses ---")
add_response("dev@example.com", question_id, "I have 5 years of experience.", "http://interview.dev")
add_response("fullstack@example.com", question_id, "Built many full-stack apps.", "http://interview.fs")

print("\n--- Get Individual Response ---")
print(get_response_by_question_and_user(question_id, "dev@example.com"))

print("\n--- All Responses ---")
print(get_all_responses())

# === Test response status ===
print("\n--- Response Status for Question ---")
print(get_response_status_for_question(question_id))
