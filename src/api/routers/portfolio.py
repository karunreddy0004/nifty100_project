from fastapi import APIRouter, HTTPException
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Portfolio"])


# ======================================================
# COMPLETE RANKING
# ======================================================
@router.get("/portfolio")
def get_portfolio():

    conn = get_connection()

    query = """
    SELECT
        r.company_id,
        c.company_name,

        r.year,
        r.quality_score,
        r.quality_rank,

        r.return_on_equity_pct,
        r.return_on_capital_employed_pct,
        r.net_profit_margin_pct,
        r.debt_to_equity

    FROM rankings r

    LEFT JOIN companies c
        ON r.company_id = c.id

    ORDER BY r.quality_rank
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df.fillna("").to_dict(orient="records")


# ======================================================
# TOP 10 PORTFOLIO
# ======================================================
@router.get("/portfolio/top10")
def get_top10():

    conn = get_connection()

    query = """
    SELECT
        r.company_id,
        c.company_name,

        r.quality_score,
        r.quality_rank,

        r.return_on_equity_pct,
        r.return_on_capital_employed_pct

    FROM rankings r

    LEFT JOIN companies c
        ON r.company_id = c.id

    ORDER BY r.quality_rank
    LIMIT 10
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df.fillna("").to_dict(orient="records")


# ======================================================
# SINGLE COMPANY RANK
# ======================================================
@router.get("/portfolio/{ticker}")
def get_company_rank(ticker: str):

    conn = get_connection()

    query = """
    SELECT
        r.*,
        c.company_name

    FROM rankings r

    LEFT JOIN companies c
        ON r.company_id = c.id

    WHERE r.company_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker.upper()]
    )

    conn.close()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return df.fillna("").iloc[0].to_dict()