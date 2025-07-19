from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

def clear_database():
    collections = ["roles", "recipients", "questions", "responses"]
    for collection_name in collections:
        collection = db[collection_name]
        result = collection.delete_many({})
        print(f"Cleared {result.deleted_count} documents from '{collection_name}' collection.")

if __name__ == "__main__":
    confirm = input("Are you sure you want to clear the entire database? This action cannot be undone! (yes/no): ")
    if confirm.lower() == "yes":
        clear_database()
        print("Database cleared.")
    else:
        print("Operation canceled.")
