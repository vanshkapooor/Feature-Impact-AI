import os
import re
import json
from groq import Groq
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# ---------------- JSON RESPONSE ---------------- #
def run_llm(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown
    content = content.replace("```json", "")
    content = content.replace("```", "")

    # Extract JSON safely
    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:
        json_text = match.group()

        try:
            parsed = json.loads(json_text)
            return json.dumps(parsed)

        except:
            return None

    return None

# ---------------- TEXT RESPONSE ---------------- #
def run_text_llm(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content