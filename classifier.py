import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

CLASSIFIER_PROMPT = """
Classify the user's intent.

Choose one label from:
- code: for programming, software development, algorithms, bug fixing, or any coding question
- data: for data science, analysis, statistics
- writing: for essays, reports, grammar, editing text (NOT writing code)
- career: for job advice, resume tips
- unclear: if it does not fit the above

Respond ONLY with JSON:

{
 "intent": "label",
 "confidence": number between 0 and 1
}
"""

def classify_intent(message):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": CLASSIFIER_PROMPT},
                    {"role": "user", "content": message}
                ]
            }
        )
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {"intent": "unclear", "confidence": 0.0}