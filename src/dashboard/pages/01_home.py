import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

# Make src importable
sys.path.append(str(Path(__file__).resolve().parents[2]))

from dashboard.utils.db import (
    get_companies,
    get_latest_financial_ratios,
    get_latest_rankings,
    get_sector_summary,
)

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Nifty 100 Analytics Dashboard")

st.sidebar.title("Dashboard Controls")
selected_year = st.sidebar.selectbox(
    "Financial Year",
    [2024, 2023, 2022, 2021, 2020, 2019],
)
st.sidebar.info(
    "This dashboard currently shows the latest available data. "
    "Year filtering will be connected in a later step."
)

# -----------------------------
# Load Data
# -----------------------------
companies = get_companies()
ratios = get_latest_financial_ratios()
rankings = get_latest_rankings()
sectors = get_sector_summary()

# -----------------------------
# KPI Cards
# -----------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Companies", len(companies))

with c2:
    st.metric(
        "Average ROE",
        f"{ratios['return_on_equity_pct'].dropna().mean():.2f}%"
    )

with c3:
    st.metric(
        "Average ROCE",
        f"{ratios['return_on_capital_employed_pct'].dropna().mean():.2f}%"
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{ratios['revenue_cagr_5yr'].dropna().mean():.2f}%"
    )

with c5:
    debt_free = ratios["debt_to_equity"].fillna(999).le(0).sum()
    st.metric("Debt-Free Companies", int(debt_free))

with c6:
    st.metric(
        "Average Net Profit Margin",
        f"{ratios['net_profit_margin_pct'].dropna().mean():.2f}%"
    )

st.divider()

# -----------------------------
# Sector Breakdown
# -----------------------------
st.subheader("📊 Sector Breakdown")

fig = px.pie(
    sectors,
    values="company_count",
    names="broad_sector",
    hole=0.5,
    title="Companies by Broad Sector",
)

fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# Top 5 Companies
# -----------------------------
st.subheader("🏆 Top 5 Companies by Quality Score")

top5 = rankings[
    [
        "company_id",
        "quality_score",
        "quality_rank",
        "return_on_equity_pct",
    ]
].head(5).copy()

top5.columns = [
    "Company",
    "Quality Score",
    "Rank",
    "ROE (%)",
]

top5["Quality Score"] = top5["Quality Score"].round(2)
top5["ROE (%)"] = top5["ROE (%)"].round(2)

st.dataframe(
    top5,
    use_container_width=True,
    hide_index=True,
)

st.caption(f"Latest data loaded. Selected year: {selected_year}")
