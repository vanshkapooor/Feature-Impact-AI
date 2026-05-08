def build_prompt(feature_name, description, users):

    return f"""
You are a senior product analyst.

Analyze this feature carefully.

Feature Name:
{feature_name}

Description:
{description}

Target Users:
{users}

IMPORTANT:
- Return ONLY valid JSON
- No markdown
- No explanation outside JSON
- Scores must be integers from 1 to 5

JSON FORMAT:

{{
    "value": 4,
    "effort": 3,
    "risk": 2,
    "adoption_prediction": "High",
    "tradeoffs": "Short explanation",
    "scenarios": {{
        "happy_path": "description",
        "edge_cases": "description",
        "misuse": "description"
    }}
}}
"""