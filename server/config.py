from dotenv import load_dotenv
import os

load_dotenv()

# Load API key from environment variable
RIBBON_API_KEY = os.getenv("RIBBON_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
