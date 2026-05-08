import streamlit as st
import re
import json
from groq import Groq

api_key = st.secrets["GROQ_API_KEY"]

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

    content = content.replace("```json", "")
    content = content.replace("```", "")

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