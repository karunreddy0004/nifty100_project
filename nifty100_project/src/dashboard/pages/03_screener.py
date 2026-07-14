import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src directory
sys.path.append(str(Path(__file__).resolve().parents[2]))

from dashboard.utils.db import (
    get_companies,
    get_latest_financial_ratios,
    get_latest_rankings,
)

st.set_page_config(
    page_title="Stock Screener",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Nifty 100 Stock Screener")

# -----------------------------
# Load Data
# -----------------------------

companies = get_companies()
ratios = get_latest_financial_ratios()
rankings = get_latest_rankings()

# Merge data

df = ratios.merge(
    rankings[
        [
            "company_id",
            "quality_score",
            "quality_rank",
        ]
    ],
    on="company_id",
    how="left",
)

df = df.merge(
    companies[
        [
            "id",
            "company_name",
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left",
)

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filter Companies")

roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    -50.0,
    100.0,
    10.0,
)

de_max = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    10.0,
    2.0,
)

npm_min = st.sidebar.slider(
    "Minimum Net Profit Margin",
    -20.0,
    100.0,
    5.0,
)

revenue_min = st.sidebar.slider(
    "Revenue CAGR (5Y)",
    -20.0,
    50.0,
    5.0,
)

fcf_min = st.sidebar.slider(
    "Minimum Free Cash Flow",
    -100000.0,
    100000.0,
    0.0,
)

# -------------------------------------------------
# Preset Filters
# -------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.subheader("Quick Presets")

preset = st.sidebar.selectbox(
    "Choose Preset",
    [
        "Custom",
        "Quality",
        "Growth",
        "Debt-Free",
        "Turnaround",
    ],
)

if preset == "Quality":
    roe_min = 20
    de_max = 1
    npm_min = 10
    revenue_min = 10

elif preset == "Growth":
    roe_min = 15
    de_max = 2
    npm_min = 8
    revenue_min = 15

elif preset == "Debt-Free":
    roe_min = 10
    de_max = 0

elif preset == "Turnaround":
    roe_min = 5
    de_max = 3
    npm_min = 0
    revenue_min = 5

# -------------------------------------------------
# Apply Filters
# -------------------------------------------------

filtered = df.copy()

filtered = filtered[
    (filtered["return_on_equity_pct"] >= roe_min)
]

filtered = filtered[
    filtered["debt_to_equity"] <= de_max
]

filtered = filtered[
    filtered["net_profit_margin_pct"] >= npm_min
]

filtered = filtered[
    filtered["revenue_cagr_5yr"] >= revenue_min
]

filtered = filtered[
    filtered["free_cash_flow"] >= fcf_min
]

filtered = filtered.sort_values(
    by="quality_rank"
)

# -------------------------------------------------
# Results
# -------------------------------------------------

st.markdown("---")

st.subheader("📈 Screening Results")

st.success(f"{len(filtered)} companies match your filters.")

display_df = filtered[
    [
        "company_id",
        "company_name",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow",
        "quality_score",
        "quality_rank",
    ]
].copy()

display_df.columns = [
    "Ticker",
    "Company",
    "ROE (%)",
    "Net Profit Margin (%)",
    "Debt / Equity",
    "Revenue CAGR (5Y)",
    "Free Cash Flow",
    "Quality Score",
    "Quality Rank",
]

# Round numeric columns
numeric_cols = [
    "ROE (%)",
    "Net Profit Margin (%)",
    "Debt / Equity",
    "Revenue CAGR (5Y)",
    "Free Cash Flow",
    "Quality Score",
]

display_df[numeric_cols] = display_df[numeric_cols].round(2)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)

# -------------------------------------------------
# CSV Download
# -------------------------------------------------

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name="nifty100_screener_results.csv",
    mime="text/csv",
)

st.caption("Sprint 4 • Day 24 • Stock Screener")