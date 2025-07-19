from roles import add_role, get_all_roles
from recipients import add_recipient, get_all_recipients
from questions import add_question, get_all_questions, get_question_by_id, update_summary, get_response_status_for_question
from responses import add_response
from pprint import pprint

# Optional: clear entire DB before testing
# clear_database()

# Step 1: Create roles
print("\n--- Adding Roles ---")
role_resp1 = add_role("Manager")
role_resp2 = add_role("Engineer")
print(role_resp1)
print(role_resp2)

all_roles = get_all_roles()
role_ids = [r["_id"] for r in all_roles]
print("Roles in DB:", role_ids)

# Step 2: Add recipients with role IDs
print("\n--- Adding Recipients ---")
add_recipient("alice@example.com", [role_ids[0]])
add_recipient("bob@example.com", [role_ids[1]])
add_recipient("carol@example.com", role_ids)  # has both roles

print("Recipients:")
pprint(get_all_recipients())

# Step 3: Add question
print("\n--- Adding Question ---")
question_resp = add_question(
    title="Team Preferences Survey",
    questions=["Do you prefer remote or in-office work?", "What tools do you use daily?"],
    flow_id="survey-001",
    creator_email="alice@example.com",
    roles=[role_ids[0]]  # send to Managers
)
print(question_resp)

question_id = question_resp["id"]

# Step 4: Get and update question
print("\n--- Fetched Question ---")
fetched = get_question_by_id(question_id)
pprint(fetched)

print("\n--- Updating Summary ---")
update_result = update_summary(question_id, "Initial insights summarized.")
print(update_result)

# Step 5: Add a response
print("\n--- Adding Response ---")
add_response(question_id, "alice@example.com", ["Remote", "Slack, Zoom"], "https://interviews.com/alice")
add_response(question_id, "carol@example.com", ["Hybrid", "Google Meet"], "https://interviews.com/carol")

# Step 6: Response status
print("\n--- Response Status ---")
status = get_response_status_for_question(question_id)
pprint(status)

# Step 7: All Questions
print("\n--- All Questions ---")
pprint(get_all_questions())
