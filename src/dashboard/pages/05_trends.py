import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Trend Analysis")

DB_PATH = Path(__file__).resolve().parents[3] / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def load_profit():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM profitandloss", conn)
    conn.close()
    return df


profit = load_profit()

companies = sorted(profit["company_id"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies,
)

metrics = {
    "Sales": "sales",
    "Operating Profit": "operating_profit",
    "Net Profit": "net_profit",
    "EPS": "eps",
}

selected_metrics = st.multiselect(
    "Select up to 3 Metrics",
    list(metrics.keys()),
    default=["Sales"],
    max_selections=3,
)

company_df = profit[
    profit["company_id"] == selected_company
].sort_values("year")

if company_df.empty:
    st.warning("No data available.")
    st.stop()

for metric_name in selected_metrics:

    fig = px.line(
        company_df,
        x="year",
        y=metrics[metric_name],
        markers=True,
        title=metric_name,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )