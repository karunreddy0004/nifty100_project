import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path


st.set_page_config(
    page_title="Investor Reports",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Investor Reports")


DB_PATH = Path(__file__).resolve().parents[3] / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)



@st.cache_data(ttl=600)
def load_reports():

    conn = get_connection()

    try:

        df = pd.read_sql(
            """
            SELECT *
            FROM investor_reports
            """,
            conn
        )

    except:

        df = pd.DataFrame()


    conn.close()

    return df



reports = load_reports()



if reports.empty:

    st.warning(
        "Investor reports table not available."
    )

    st.info(
        "Load investor_reports.xlsx into SQLite first."
    )

    st.stop()



company = st.selectbox(
    "Select Company",
    sorted(
        reports["company_id"].unique()
    )
)



report = reports[
    reports["company_id"] == company
].iloc[0]



st.subheader(
    f"📊 {company} Investment Report"
)


col1, col2, col3 = st.columns(3)


col1.metric(
    "Rating",
    report["rating"]
)


col2.metric(
    "Final Score",
    report["final_score"]
)


col3.metric(
    "Risk Score",
    report["risk_score"]
)



st.divider()


st.subheader(
    "AI Generated Analysis"
)


st.text(
    report["investor_report"]
)



# Export

st.download_button(
    "⬇️ Download Report",
    report["investor_report"],
    file_name=f"{company}_investor_report.txt"
)