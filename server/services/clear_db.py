# clear_database.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

def clear_database():
    collections = ["roles", "recipients", "questions", "responses"]
    for col in collections:
        result = db[col].delete_many({})
        print(f"Cleared {col}: {result.deleted_count} documents")

if __name__ == "__main__":
    confirm = input("Are you sure you want to clear the database? This cannot be undone. (y/n): ")
    if confirm.lower() == 'y':
        clear_database()
    else:
        print("Operation cancelled.")
