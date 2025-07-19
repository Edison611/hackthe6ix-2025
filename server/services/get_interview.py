import requests
from dotenv import load_dotenv
import os

load_dotenv()

RIBBON_API_KEY = os.getenv("RIBBON_API_KEY")

url = "https://app.ribbon.ai/be-api/v1/interviews"
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {RIBBON_API_KEY}",
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())
