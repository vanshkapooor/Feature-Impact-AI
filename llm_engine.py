import os
import re
import json
import streamlit as st

from groq import Groq
from dotenv import load_dotenv

# ---------------- LOAD ENV ---------------- #
load_dotenv()

# ---------------- API KEY HANDLING ---------------- #
try:
    # For Streamlit Cloud
    api_key = st.secrets["GROQ_API_KEY"]

except:
    # For local development
    api_key = os.getenv("GROQ_API_KEY")

# ---------------- GROQ CLIENT ---------------- #
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

    # Extract JSON
    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:

        try:
            parsed = json.loads(match.group())
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