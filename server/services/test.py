import os
from bson import ObjectId
from unittest.mock import patch
from recipients import add_recipient, get_all_recipients
from questions import add_question, update_summary, get_question_by_id, get_response_status_for_question, get_all_questions, summarize_question_responses
from responses import add_response, get_responses_by_question_id, update_response_summary

def test_summarize_with_fake_data():
    # Add a recipient (if not exists)
    recipient_email = "fakeuser@example.com"
    recipients = get_all_recipients()
    if not any(r["email"] == recipient_email for r in recipients):
        add_recipient(recipient_email, role_ids=[])  # Add with no roles for simplicity

    # Add a question
    question_data = add_question(
        title="Test Summary Question",
        questions=["What is your favorite hobby?", "Why do you enjoy it?"],
        flow_id="test-flow",
        creator_email=recipient_email,
        roles=[]
    )
    question_id = question_data.get("id")
    print("Added question:", question_id)

    # Add some fake responses
    transcripts = [
        "I really enjoy painting because it helps me relax.",
        "My hobby is hiking. It lets me connect with nature and stay fit.",
        "I love playing chess as it challenges my mind."
    ]

    for t in transcripts:
        add_response(
            user_email=recipient_email,
            question_id=question_id,
            transcript=t,
            interview_url="http://example.com/interview"
        )
    
    # Patch the Gemini API call inside summarize_question_responses to mock the AI summary
    fake_summary = "People enjoy hobbies like painting, hiking, and chess because they provide relaxation, nature connection, fitness, and mental challenge."

    with patch("questions.genai.GenerativeModel.generate_content") as mock_genai:
        class FakeResponse:
            def __init__(self, text):
                self.text = text
        
        mock_genai.return_value = FakeResponse(fake_summary)

        # Call the summary function
        summary_result = summarize_question_responses(question_id)
        print("Summary result:", summary_result)

if __name__ == "__main__":
    test_summarize_with_fake_data()
