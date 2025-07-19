from pymongo import MongoClient
from dotenv import load_dotenv
import os

def delete_test_documents():
    load_dotenv()
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print("MONGODB_URI not found in environment variables.")
        return

    try:
        client = MongoClient(mongodb_uri)
        db = client.get_database()

        test_col = db["test_collection"]
        result = test_col.delete_many({"test_field": "test_value"})
        print(f"Deleted {result.deleted_count} document(s) from test_collection.")

    except Exception as e:
        print(f"Failed to delete test documents: {e}")

if __name__ == "__main__":
    delete_test_documents()