import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏢",
    layout="wide",
)

st.title("🏢 Sector Analysis")

DB_PATH = Path(__file__).resolve().parents[3] / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def load_sector_data():

    conn = get_connection()

    query = """
    SELECT
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        p.sales,
        r.return_on_equity_pct,
        m.market_cap_crore
    FROM companies c
    JOIN sectors s
        ON c.id = s.company_id
    JOIN financial_ratios r
        ON c.id = r.company_id
    JOIN profitandloss p
        ON c.id = p.company_id
        AND r.year = p.year
    JOIN market_cap m
        ON c.id = m.company_id
    WHERE r.year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


sector_df = load_sector_data()

sector = st.selectbox(
    "Select Sector",
    sorted(sector_df["broad_sector"].unique())
)

filtered = sector_df[
    sector_df["broad_sector"] == sector
]

fig = px.scatter(
    filtered,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    title=f"{sector} Sector Analysis",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("Sector Companies")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)