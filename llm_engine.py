import os
import re
import json
import streamlit as st

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    api_key = st.secrets["GROQ_API_KEY"]

except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

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