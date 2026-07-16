import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from pathlib import Path

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="👥",
    layout="wide",
)

st.title("👥 Peer Comparison")

# ---------------------------------------------------
# Database
# ---------------------------------------------------

DB_PATH = Path(__file__).resolve().parents[3] / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ---------------------------------------------------
# Load Peer Groups
# ---------------------------------------------------

@st.cache_data(ttl=600)
def load_peer_groups():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_groups
        ORDER BY peer_group_name, company_id
        """,
        conn,
    )

    conn.close()

    return df


# ---------------------------------------------------
# Load Scorecard
# ---------------------------------------------------

@st.cache_data(ttl=600)
def load_scorecard():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM scorecard
        """,
        conn,
    )

    conn.close()

    return df


peer_df = load_peer_groups()
score_df = load_scorecard()

# ---------------------------------------------------
# Peer Group Selection
# ---------------------------------------------------

peer_groups = sorted(peer_df["peer_group_name"].unique())

selected_group = st.sidebar.selectbox(
    "Select Peer Group",
    peer_groups,
)

companies = peer_df[
    peer_df["peer_group_name"] == selected_group
]

company_list = companies["company_id"].tolist()

selected_company = st.selectbox(
    "Select Company",
    company_list,
)

benchmark_row = companies[
    companies["is_benchmark"] == 1
]

benchmark_company = None

if not benchmark_row.empty:
    benchmark_company = benchmark_row.iloc[0]["company_id"]

st.success(f"Benchmark Company: {benchmark_company}")

# ---------------------------------------------------
# Latest Data
# ---------------------------------------------------

company_data = score_df[
    score_df["company_id"] == selected_company
].sort_values("year")

benchmark_data = score_df[
    score_df["company_id"] == benchmark_company
].sort_values("year")

if company_data.empty or benchmark_data.empty:
    st.warning("Data not available.")
    st.stop()

company_latest = company_data.iloc[-1]
benchmark_latest = benchmark_data.iloc[-1]

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "asset_turnover",
    "interest_coverage",
    "free_cash_flow",
    "cfo_pat_ratio",
]

company_values = [company_latest[m] for m in metrics]
benchmark_values = [benchmark_latest[m] for m in metrics]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=metrics,
        fill="toself",
        name=selected_company,
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=benchmark_values,
        theta=metrics,
        fill="toself",
        name=benchmark_company,
    )
)

fig.update_layout(
    title="Company vs Benchmark",
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=650,
)

st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------
# Peer Comparison Table
# ---------------------------------------------------

st.subheader("📋 Peer Comparison Table")

peer_latest = (
    score_df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

peer_latest = peer_latest[
    peer_latest["company_id"].isin(company_list)
]

table = peer_latest[
    [
        "company_id",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "asset_turnover",
        "interest_coverage",
        "free_cash_flow",
        "cfo_pat_ratio",
    ]
].copy()

table["Status"] = ""

table.loc[
    table["company_id"] == selected_company,
    "Status"
] = "Selected"

table.loc[
    table["company_id"] == benchmark_company,
    "Status"
] = "Benchmark"

table = table[
    [
        "Status",
        "company_id",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "asset_turnover",
        "interest_coverage",
        "free_cash_flow",
        "cfo_pat_ratio",
    ]
]

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
)
