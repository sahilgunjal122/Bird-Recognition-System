from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Optional: Print warning if missing
if not all([GOOGLE_API_KEY, GOOGLE_CX, GEMINI_API_KEY]):
    print("⚠️ One or more API keys are missing from your .env file!")