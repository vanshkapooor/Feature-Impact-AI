import streamlit as st
import json
import plotly.graph_objects as go

from prompt_templates import build_prompt
from llm_engine import run_llm
from simulator import simulate_outcomes
from scorer import calculate_score
from insights import generate_chart_insights
from explanation_engine import generate_explanation

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Feature Impact Analysis AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #1d4ed8;
    color: white;
}

.metric-card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

.insight-box {
    background-color: white;
    color: black;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    border-left: 6px solid #2563eb;
    font-size: 16px;
    font-weight: 500;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.title("🚀 Feature Impact Analysis AI System")
st.markdown("""
Analyze product features before development using AI-powered evaluation,
risk prediction, and decision intelligence.
""")

# ---------------- SIDEBAR ---------------- #
st.sidebar.header("📌 About System")

st.sidebar.info("""
This AI system helps product teams:

✅ Evaluate feature value  
✅ Predict implementation effort  
✅ Detect risks early  
✅ Simulate user outcomes  
✅ Generate AI-based recommendations  
""")

# ---------------- INPUT SECTION ---------------- #
st.subheader("📝 Enter Feature Details")

feature_name = st.text_input("📌 Feature Name")

description = st.text_area(
    "🧾 Feature Description",
    height=150
)

users = st.text_input("👥 Target Users")

# ---------------- ANALYZE BUTTON ---------------- #
if st.button("🔍 Analyze Feature"):

    if not feature_name or not description or not users:
        st.warning("⚠️ Please fill all fields.")
    else:

        # Build prompt
        prompt = build_prompt(
            feature_name,
            description,
            users
        )

        # LLM Processing
        with st.spinner("🤖 Running AI analysis..."):
            raw_output = run_llm(prompt)

        try:
            # Parse JSON
            if raw_output is None:
                st.error("⚠️ AI failed to generate valid JSON.")
                st.stop()

            data = json.loads(raw_output)

            value = int(data["value"])
            effort = int(data["effort"])
            risk = int(data["risk"])

            # Simulation
            sim_results = simulate_outcomes(data)

            # Final priority
            priority = calculate_score(
                value,
                effort,
                risk
            )

            # Generate insights
            insights = generate_chart_insights(
                value,
                effort,
                risk,
                sim_results
            )

            # ---------------- METRICS ---------------- #
            st.subheader("📊 Key Metrics")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("💎 Value", value)

            with c2:
                st.metric("🛠️ Effort", effort)

            with c3:
                st.metric("⚠️ Risk", risk)

            with c4:
                st.metric("🎯 Priority", priority)

            # ---------------- CHARTS ---------------- #
            st.subheader("📈 Visual Analytics")

            col1, col2 = st.columns(2)

            # ---------------- BAR CHART ---------------- #
            with col1:

                fig_bar = go.Figure()

                fig_bar.add_trace(go.Bar(
                    x=["Value", "Effort", "Risk"],
                    y=[value, effort, risk],
                    text=[value, effort, risk],
                    textposition="outside",
                    marker=dict(
                        color=["#00cc96", "#ffa15a", "#ef553b"],
                        line=dict(color="black", width=1.5)
                    )
                ))

                fig_bar.update_layout(
                    title="📊 Feature Evaluation Scores",
                    yaxis=dict(
                        title="Score",
                        range=[0, 5]
                    ),
                    xaxis=dict(title="Metrics"),
                    template="plotly_white",
                    height=450
                )

                st.plotly_chart(
                    fig_bar,
                    use_container_width=True
                )

            # ---------------- RADAR CHART ---------------- #
            with col2:

                fig_radar = go.Figure()

                fig_radar.add_trace(go.Scatterpolar(
                    r=[value, effort, risk],
                    theta=["Value", "Effort", "Risk"],
                    fill='toself',
                    fillcolor="rgba(37,99,235,0.3)",
                    line=dict(
                        color="#2563eb",
                        width=3
                    )
                ))

                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )
                    ),
                    title="🧭 Feature Balance Overview",
                    template="plotly_white",
                    height=450
                )

                st.plotly_chart(
                    fig_radar,
                    use_container_width=True
                )

            # ---------------- DONUT CHART ---------------- #
            st.subheader("⚠️ Simulation Risk Distribution")

            mapping = {
                "Low": 1,
                "Medium": 2,
                "High": 3
            }

            labels = []
            values = []

            for k, v in sim_results.items():
                labels.append(
                    k.replace("_", " ").title()
                )
                values.append(
                    mapping.get(v, 2)
                )

            fig_donut = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                textinfo="label+percent"
            )])

            fig_donut.update_layout(
                title="Risk & Simulation Insights",
                template="plotly_white",
                height=500
            )

            st.plotly_chart(
                fig_donut,
                use_container_width=True
            )

            # ---------------- RAW AI OUTPUT ---------------- #
            st.subheader("🧠 AI Evaluation Report")

            st.json(data)

            # ---------------- INSIGHTS ---------------- #
            st.subheader("💡 AI-Generated Insights")

            for insight in insights:
                st.markdown(
                    f"""
                    <div class="insight-box">
                    {insight}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ---------------- LLM EXPLANATION ---------------- #
            st.subheader("🧠 LLM-Based Explanation")

            with st.spinner("Generating detailed explanation..."):

                explanation = generate_explanation(
                    feature_name,
                    data,
                    sim_results
                )

            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:20px;
                    border-radius:12px;
                    color:black;
                    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
                ">
                {explanation}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error("⚠️ Failed to parse model output.")

            st.subheader("Raw Model Output")
            st.code(raw_output)

            st.exception(e)