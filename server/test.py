<<<<<<< Updated upstream
from roles import add_role, delete_role
from recipients import add_recipient, delete_recipient
from questions import add_question, update_summary, get_response_status_for_question
from responses import add_response, delete_response, update_response_summary

def run_full_test():
    print("=== RUNNING FULL INTEGRATION TEST ===")

    # Step 1: Add roles
    print("\n-- Adding Roles --")
    print(add_role(1, "Admin"))
    print(add_role(2, "Interviewer"))

    # Step 2: Add recipients
    recipient_1 = "user1@example.com"
    recipient_2 = "user2@example.com"
    print("\n-- Adding Recipients --")
    print(add_recipient(recipient_1, [1]))
    print(add_recipient(recipient_2, [2]))

    # Step 3: Add question with unique question_id
    question_data = [
        "What inspired you to apply for this role?",
        "How do you handle difficult challenges?"
    ]
    print("\n-- Adding Question --")
    add_question_result = add_question(
        questions=question_data,
        flow_id="flow_xyz123",
        creator_email=recipient_1
    )
    print(add_question_result)
    question_id = add_question_result.get("question_id")
    if not question_id:
        print("Failed to create question, aborting test.")
        return

    # Step 4: Update question summary
    print("\n-- Updating Question Summary --")
    print(update_summary(question_id, "Summary: candidate motivation and resilience."))

    # Step 5: Check who has responded (expect none initially)
    print("\n-- Checking Response Status (initial) --")
    status = get_response_status_for_question(question_id)
    print(status)  # Should show both recipients as 'not_responded'

    # Step 6: Add response from recipient 1
    print("\n-- Adding Response from Recipient 1 --")
    add_response_result = add_response(
        user_email=recipient_1,
        question_id=question_id,
        transcript="I am very motivated by challenge and growth.",
        interview_url="https://interviewlink.example.com/123"
    )
    print(add_response_result)
    response_id = add_response_result.get("id")
    if not response_id:
        print("Failed to add response, aborting test.")
        return

    # Step 7: Update response summary
    print("\n-- Updating Response Summary --")
    print(update_response_summary(response_id, "Response summary: strong motivation."))

    # Step 8: Check who has responded (recipient 1 should be responded now)
    print("\n-- Checking Response Status (after 1 response) --")
    status = get_response_status_for_question(question_id)
    print(status)  # recipient_1 in responded, recipient_2 in not_responded

    # Step 9: Delete response
    print("\n-- Deleting Response --")
    print(delete_response(response_id))

    # Step 10: Delete recipients
    print("\n-- Deleting Recipients --")
    print(delete_recipient(recipient_1))
    print(delete_recipient(recipient_2))

    # Step 11: Delete roles
    print("\n-- Deleting Roles --")
    print(delete_role(1))
    print(delete_role(2))

    print("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    run_full_test()
=======
from roles import add_role, get_all_roles, get_role_by_id, delete_role
from recipients import add_recipient, get_all_recipients, get_recipient_by_email, delete_recipient
from questions import add_question, get_all_questions, get_question_by_id, update_summary, get_response_status_for_question
from responses import add_response, update_response_summary, delete_response, get_response_by_id, get_responses_by_question_id, get_all_responses

def print_section(title):
    print("\n" + "-" * 10 + f" {title} " + "-" * 10)

def run_test():
    print_section("Adding Roles")
    role1 = add_role("Developer")
    role2 = add_role("Designer")
    print(role1)
    print(role2)

    role1_id = role1["id"]
    role2_id = role2["id"]

    print_section("Adding Recipients")
    rec1 = add_recipient("user1@example.com", [role1_id])
    rec2 = add_recipient("user2@example.com", [role2_id])
    print(rec1)
    print(rec2)

    print_section("Adding Question")
    question = add_question(
        questions=["What is your experience with Python?", "Describe a challenging project you worked on."],
        flow_id="flow_001",
        creator_email="user1@example.com",
        roles=[role1_id]
    )
    print(question)
    question_id = question["question_id"]

    print_section("Updating Question Summary")
    update_result = update_summary(question_id, "Summary: Python experience and challenge response.")
    print(update_result)

    print_section("Getting Question by ID")
    question_data = get_question_by_id(question_id)
    print(question_data)

    print_section("Getting All Questions")
    all_questions = get_all_questions()
    print(all_questions)

    print_section("Adding Responses")
    response1 = add_response("user1@example.com", question_id, "I have 5 years experience.", "http://interview1.example.com")
    response2 = add_response("user2@example.com", question_id, "I worked on complex systems.", "http://interview2.example.com")
    print(response1)
    print(response2)

    response1_id = response1["id"]
    response2_id = response2["id"]

    print_section("Updating Response Summary")
    update_resp1 = update_response_summary(response1_id, "Strong Python skills.")
    update_resp2 = update_response_summary(response2_id, "Good project experience.")
    print(update_resp1)
    print(update_resp2)

    print_section("Getting Responses by Question ID")
    responses_for_question = get_responses_by_question_id(question_id)
    print(responses_for_question)

    print_section("Getting Response by ID")
    resp1_data = get_response_by_id(response1_id)
    print(resp1_data)

    print_section("Getting Response Status for Question")
    status = get_response_status_for_question(question_id)
    print(status)

    print_section("Deleting Responses")
    del_resp1 = delete_response(response1_id)
    del_resp2 = delete_response(response2_id)
    print(del_resp1)
    print(del_resp2)

    print_section("Deleting Recipients")
    del_rec1 = delete_recipient("user1@example.com")
    del_rec2 = delete_recipient("user2@example.com")
    print(del_rec1)
    print(del_rec2)

    print_section("Deleting Roles")
    del_role1 = delete_role(role1_id)
    del_role2 = delete_role(role2_id)
    print(del_role1)
    print(del_role2)

    print_section("Test Complete")

if __name__ == "__main__":
    run_test()
>>>>>>> Stashed changes
