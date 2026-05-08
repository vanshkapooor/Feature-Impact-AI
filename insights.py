def generate_chart_insights(value, effort, risk, sim_results):
    insights = []

    if value >= 4:
        insights.append("High business value — strong impact expected.")
    elif value <= 2:
        insights.append("Low business value — limited ROI.")

    if effort >= 4:
        insights.append("High effort — requires significant engineering work.")
    elif effort <= 2:
        insights.append("Low effort — quick implementation possible.")

    if risk >= 4:
        insights.append("High risk — potential issues in security or UX.")
    elif risk <= 2:
        insights.append("Low risk — safe feature to implement.")

    if value >= 4 and effort <= 2:
        insights.append("Best case: high value with low effort.")
    elif value >= 4 and effort >= 4:
        insights.append("High value but costly — needs prioritization.")

    if risk >= 4:
        insights.append("Recommendation: mitigate risks before development.")

    return insights