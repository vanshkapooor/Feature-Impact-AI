def calculate_score(value, effort, risk):
    priority_score = (value * 2) - (effort + risk)

    if priority_score >= 5:
        return "🔥 High Priority"
    elif priority_score >= 2:
        return "⚖️ Medium Priority"
    else:
        return "❌ Low Priority"