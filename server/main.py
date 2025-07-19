# === main.py ===
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import subprocess
import json
import os
from dotenv import load_dotenv
<<<<<<< Updated upstream
=======
from pymongo import MongoClient
>>>>>>> Stashed changes

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from environment variable
RIBBON_API_KEY = os.getenv("RIBBON_API_KEY")

# In-memory storage for mock data
database = {
    "questions": [],
    "responses": [
        {"name": "Alice", "answer": "Blocked by API quota", "score": 7},
        {"name": "Bob", "answer": "Need help with login bugs", "score": 8},
        {"name": "Charlie", "answer": "Everything smooth", "score": 6},
    ],
    "summary": "Most team members are progressing, but API and login bugs are common blockers.",
    "trends": [
        {"theme": "API Issues", "description": "Frequent blockers due to rate limits", "count": 4},
        {"theme": "Login Problems", "description": "Ongoing user complaints about sign-in flow", "count": 3},
    ],
}

class QuestionRequest(BaseModel):
    question: str

class VideoRequest(BaseModel):
    video_url: str

@app.post("/questions")
async def create_question(payload: QuestionRequest):
    database["questions"].append(payload.question)
    # Optionally: Call Ribbon API to create interview here
    return {"message": "Question submitted successfully."}

@app.get("/responses")
async def get_responses():
    return {
        "responses": database["responses"],
        "summary": database["summary"]
    }

@app.get("/trends")
async def get_trends():
    return {
        "trends": database["trends"]
    }

@app.post("/process")
async def process_video(data: VideoRequest):
    curl_command = [
        "curl",
        "-X", "POST",
        "https://api.ribbon.ai/v1/interviews/transcribe",
        "-H", f"Authorization: Bearer {RIBBON_API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"video_url": data.video_url})
    ]

    try:
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = json.loads(result.stdout)
        summary = output.get("summary", "No summary available.")
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}
