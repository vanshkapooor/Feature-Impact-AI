def simulate_outcomes(data):
    scenarios = data.get("scenarios", {})

    return {
        "drop_off_risk": "Medium" if data["risk"] >= 3 else "Low",
        "user_confusion": "High" if "complex" in scenarios.get("edge_cases", "").lower() else "Low",
        "performance_impact": "Moderate" if data["effort"] >= 3 else "Low"
    }