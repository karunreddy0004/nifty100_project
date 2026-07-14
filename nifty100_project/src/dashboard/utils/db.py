import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# -----------------------------------------------------
# Database Path
# -----------------------------------------------------
DB_PATH = Path(__file__).resolve().parents[3] / "db" / "nifty100.db"


# -----------------------------------------------------
# Database Connection
# -----------------------------------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)


# -----------------------------------------------------
# Companies
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


# -----------------------------------------------------
# Financial Ratios
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [ticker]

    if year is not None:
        query += " AND year = ?"
        params.append(year)

    df = pd.read_sql(query, conn, params=params)

    conn.close()

    return df


# -----------------------------------------------------
# Profit & Loss
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM profitandloss WHERE company_id=?",
        conn,
        params=[ticker],
    )

    conn.close()

    return df


# -----------------------------------------------------
# Balance Sheet
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM balancesheet WHERE company_id=?",
        conn,
        params=[ticker],
    )

    conn.close()

    return df


# -----------------------------------------------------
# Cash Flow
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM cashflow WHERE company_id=?",
        conn,
        params=[ticker],
    )

    conn.close()

    return df


# -----------------------------------------------------
# Sectors
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    df = pd.read_sql("SELECT * FROM sectors", conn)

    conn.close()

    return df


# -----------------------------------------------------
# Peer Groups
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM peer_groups WHERE broad_sector=?",
        conn,
        params=[group_name],
    )

    conn.close()

    return df


# -----------------------------------------------------
# Valuation
# -----------------------------------------------------
@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = get_connection()

    try:
        df = pd.read_sql(
            "SELECT * FROM valuation_summary WHERE company_id=?",
            conn,
            params=[ticker],
        )
    except Exception:
        df = pd.DataFrame()

    conn.close()

    return df

# -----------------------------------------------------
# Home Dashboard Data
# -----------------------------------------------------

@st.cache_data(ttl=600)
def get_latest_rankings():
    conn = get_connection()

    query = """
    SELECT *
    FROM rankings
    WHERE year = (SELECT MAX(year) FROM rankings)
    ORDER BY quality_rank
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_latest_financial_ratios():
    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year = (SELECT MAX(year) FROM financial_ratios)
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sector_summary():
    conn = get_connection()

    query = """
    SELECT broad_sector,
           COUNT(company_id) AS company_count
    FROM sectors
    GROUP BY broad_sector
    ORDER BY company_count DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df