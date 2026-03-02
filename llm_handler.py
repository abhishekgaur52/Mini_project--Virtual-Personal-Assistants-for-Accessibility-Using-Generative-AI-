# llm_handler.py
import os
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_ai(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Answer in one clear sentence: {question}"
        )
        return response.text.strip()
    except Exception as e:
        print("AI Error:", e)
        return None
