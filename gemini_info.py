import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_bird_info(bird_name):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        prompt = f"Give me detailed information about the bird called {bird_name}."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Error getting Gemini info:", e)
        return "No information available at the moment."
