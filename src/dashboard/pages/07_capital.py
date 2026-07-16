import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Capital Allocation",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Capital Allocation Map")

DB_PATH = Path(__file__).resolve().parents[3] / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def load_data():

    conn = get_connection()

    query = """
    SELECT
        c.company_name,
        s.broad_sector,
        r.free_cash_flow,
        r.return_on_equity_pct,
        r.debt_to_equity
    FROM companies c
    JOIN financial_ratios r
        ON c.id = r.company_id
    JOIN sectors s
        ON c.id = s.company_id
    WHERE r.year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


df = load_data()


def allocation_pattern(row):

    if row["free_cash_flow"] > 0 and row["debt_to_equity"] < 0.5:
        return "Strong Cash Generator"

    elif row["return_on_equity_pct"] > 20:
        return "High ROE"

    elif row["debt_to_equity"] > 1:
        return "Highly Leveraged"

    else:
        return "Balanced"


df["Pattern"] = df.apply(allocation_pattern, axis=1)

# Create positive values for treemap size
df["TreeSize"] = df["free_cash_flow"].fillna(0).abs() + 1

fig = px.treemap(
    df,
    path=["Pattern", "company_name"],
    values="TreeSize",
    color="return_on_equity_pct",
    hover_data=["free_cash_flow", "debt_to_equity"],
)
st.plotly_chart(
    fig,
    use_container_width=True,
)

pattern = st.selectbox(
    "Select Pattern",
    sorted(df["Pattern"].unique())
)

st.subheader(f"{pattern} Companies")

st.dataframe(
    df[df["Pattern"] == pattern],
    use_container_width=True,
    hide_index=True,
)