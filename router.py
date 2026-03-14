import os
import requests
from dotenv import load_dotenv
from prompts import PROMPTS
from logger import log_route

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def route_and_respond(message, intent_data):
    intent = intent_data["intent"]
    confidence = intent_data["confidence"]

    if intent == "unclear":
        response = "I'm not sure what you need. Are you asking about coding, data analysis, writing help, or career advice?"
        log_route(intent, confidence, message, response)
        return response

    system_prompt = PROMPTS[intent]
    completion = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        }
    )

    data = completion.json()
    if "error" in data:
        return "Sorry, I encountered an API error: " + str(data.get("error"))
        
    if "choices" not in data:
        return "Sorry, I encountered an unexpected error."

    final_response = data["choices"][0]["message"]["content"]
    log_route(intent, confidence, message, final_response)
    return final_response