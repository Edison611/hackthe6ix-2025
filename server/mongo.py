from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()

# Collections
recipients = db["recipients"]
roles = db["roles"]
questions = db["questions"]
responses = db["responses"]
summary = db["summary"]
