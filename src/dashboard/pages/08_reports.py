import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path


# -----------------------------------------------------
# Page Config
# -----------------------------------------------------

st.set_page_config(
    page_title="Reports Dashboard",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Investment Reports Dashboard")


# -----------------------------------------------------
# Paths
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"



# -----------------------------------------------------
# Database Connection
# -----------------------------------------------------

def get_connection():

    return sqlite3.connect(DB_PATH)



# -----------------------------------------------------
# Load Functions
# -----------------------------------------------------

@st.cache_data(ttl=600)
def load_portfolio():

    file = OUTPUT_DIR / "final_portfolio.xlsx"

    if file.exists():
        return pd.read_excel(file)

    return pd.DataFrame()



@st.cache_data(ttl=600)
def load_valuation():

    file = OUTPUT_DIR / "valuation_summary.xlsx"

    if file.exists():
        return pd.read_excel(file)

    return pd.DataFrame()



@st.cache_data(ttl=600)
def load_backtest():

    file = OUTPUT_DIR / "backtest_results.xlsx"

    if file.exists():
        return pd.read_excel(file)

    return pd.DataFrame()



@st.cache_data(ttl=600)
def load_company_summary():

    conn = get_connection()

    try:

        df = pd.read_sql(
            """
            SELECT *
            FROM company_summary
            """,
            conn
        )

    except:

        df = pd.DataFrame()


    conn.close()

    return df



@st.cache_data(ttl=600)
def load_pros_cons():

    conn = get_connection()

    try:

        df = pd.read_sql(
            """
            SELECT *
            FROM pros_cons
            """,
            conn
        )

    except:

        df = pd.DataFrame()


    conn.close()

    return df



@st.cache_data(ttl=600)
def load_documents():

    conn = get_connection()

    try:

        df = pd.read_sql(
            """
            SELECT *
            FROM documents
            ORDER BY company_id, year DESC
            """,
            conn
        )

    except:

        df = pd.DataFrame()


    conn.close()

    return df



# -----------------------------------------------------
# Portfolio Section
# -----------------------------------------------------

st.header("🏆 Portfolio Recommendation")


portfolio = load_portfolio()


if not portfolio.empty:

    st.dataframe(
        portfolio,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "Portfolio report not available."
    )



# -----------------------------------------------------
# Valuation Section
# -----------------------------------------------------

st.header("💰 Valuation Report")


valuation = load_valuation()


if not valuation.empty:


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Total Companies",
            len(valuation)
        )


    with col2:

        if "valuation_status" in valuation.columns:

            st.metric(
                "Fairly Valued",
                len(
                    valuation[
                        valuation["valuation_status"]
                        ==
                        "Fairly Valued"
                    ]
                )
            )


    st.dataframe(
        valuation,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "Valuation report not available."
    )



# -----------------------------------------------------
# Backtest Section
# -----------------------------------------------------

st.header("📈 Backtest Performance")


backtest = load_backtest()


if not backtest.empty:


    st.dataframe(
        backtest,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "Backtest results not available."
    )



# -----------------------------------------------------
# AI Summary Section
# -----------------------------------------------------

st.header("🤖 AI Company Intelligence")


summary = load_company_summary()


if not summary.empty:


    company = st.selectbox(
        "Select Company",
        sorted(
            summary["company_id"].unique()
        ),
        key="summary_company"
    )


    result = summary[
        summary["company_id"] == company
    ]


    st.success(
        result.iloc[0]["summary"]
    )


else:

    st.info(
        "Company summaries not available."
    )



# -----------------------------------------------------
# Pros Cons Section
# -----------------------------------------------------

st.header("⚖️ Pros & Cons Analysis")


pros_cons = load_pros_cons()


if not pros_cons.empty:


    selected = st.selectbox(
        "Select Company",
        sorted(
            pros_cons["company_id"].unique()
        ),
        key="pros_cons_company"
    )

    data = pros_cons[
        pros_cons["company_id"] == selected
    ]


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("✅ Pros")

        for _, row in data[
            data["type"] == "Pro"
        ].iterrows():

            st.success(
                row["text"]
            )


    with col2:

        st.subheader("⚠️ Cons")

        for _, row in data[
            data["type"] == "Con"
        ].iterrows():

            st.error(
                row["text"]
            )



# -----------------------------------------------------
# Annual Reports
# -----------------------------------------------------

st.header("📄 Annual Reports")


documents = load_documents()


if documents.empty:

    st.info(
        "No annual reports available."
    )


else:


    company = st.selectbox(
        "Company Reports",
        sorted(
            documents["company_id"].unique()
        )
    )


    company_reports = documents[
        documents["company_id"] == company
    ]


    st.dataframe(
        company_reports,
        use_container_width=True,
        hide_index=True
    )



# -----------------------------------------------------
# Downloads
# -----------------------------------------------------

st.header("⬇️ Download Reports")


for file in OUTPUT_DIR.glob("*"):

    if file.suffix in [".csv", ".xlsx"]:

        with open(file, "rb") as f:

            st.download_button(
                label=f"Download {file.name}",
                data=f,
                file_name=file.name
            )