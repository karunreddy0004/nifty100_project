import streamlit as st
import plotly.express as px
import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parents[2])
)


from dashboard.utils.db import (
    get_investment_scores,
    get_risk_analysis
)



st.set_page_config(
    page_title="Investment Intelligence",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Investment Intelligence Dashboard")


# --------------------------------------------------
# Load Data
# --------------------------------------------------

scores = get_investment_scores()
risk = get_risk_analysis()



if scores.empty:

    st.warning(
        "Investment score data not available."
    )

    st.stop()



# --------------------------------------------------
# Top Metrics
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Companies Analysed",
        len(scores)
    )


with col2:
    strong_buy = len(
        scores[
            scores["rating"]=="Strong Buy"
        ]
    )

    st.metric(
        "Strong Buy",
        strong_buy
    )


with col3:

    avg_score = round(
        scores["final_score"].mean(),
        2
    )

    st.metric(
        "Average Score",
        avg_score
    )



# --------------------------------------------------
# Top Investment Opportunities
# --------------------------------------------------

st.subheader(
    "🏆 Top Investment Opportunities"
)


st.dataframe(
    scores.head(10),
    use_container_width=True,
    hide_index=True
)



# --------------------------------------------------
# Score Chart
# --------------------------------------------------

st.subheader(
    "Final Score Ranking"
)


fig = px.bar(
    scores.head(10),
    x="company_id",
    y="final_score",
    text="final_score",
    title="Top 10 Companies"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# --------------------------------------------------
# Risk Section
# --------------------------------------------------

if not risk.empty:


    st.subheader(
        "⚠️ Risk Distribution"
    )


    risk_count = (
        risk["overall_risk"]
        .value_counts()
        .reset_index()
    )


    risk_count.columns = [
        "Risk",
        "Count"
    ]


    fig2 = px.pie(
        risk_count,
        names="Risk",
        values="Count"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



    st.subheader(
        "Risk Details"
    )


    st.dataframe(
        risk.head(20),
        use_container_width=True,
        hide_index=True
    )