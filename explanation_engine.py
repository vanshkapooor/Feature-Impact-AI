from llm_engine import run_text_llm

def generate_explanation(
    feature_name,
    data,
    sim_results
):

    prompt = f"""
You are a senior Product Manager.

Explain this feature evaluation professionally.

Feature:
{feature_name}

Scores:
- Value: {data['value']}
- Effort: {data['effort']}
- Risk: {data['risk']}

Simulation Insights:
{sim_results}

Provide:
1. Value explanation
2. Effort explanation
3. Risk explanation
4. Trade-offs
5. Final recommendation

Keep it concise and easy to understand.
"""

    return run_text_llm(prompt)