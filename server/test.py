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
