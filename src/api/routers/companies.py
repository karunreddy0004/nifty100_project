from fastapi import APIRouter, Query, HTTPException
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Companies"])


# ======================================================
# GET ALL COMPANIES
# ======================================================
@router.get("/companies")
def get_companies(
    sector: str | None = Query(None),
    market_cap_category: str | None = Query(None),
    search: str | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,
        fr.return_on_equity_pct AS roe_pct,
        fr.return_on_capital_employed_pct AS roce_pct

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE fr.year = (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id = c.id
    )

    ORDER BY c.company_name
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if sector:
        df = df[
            df["broad_sector"].str.lower() == sector.lower()
        ]

    if market_cap_category:
        df = df[
            df["market_cap_category"].str.lower()
            == market_cap_category.lower()
        ]

    if search:
        s = search.lower()
        df = df[
            df["company_name"].str.lower().str.contains(s)
            | df["id"].str.lower().str.contains(s)
        ]

    return df.fillna("").to_dict(orient="records")


# ======================================================
# GET COMPANY DETAILS
# ======================================================
@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        c.company_logo,
        c.about_company,
        c.website,
        c.face_value,
        c.book_value,
        c.roe_percentage,
        c.roce_percentage,

        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,

        fr.*

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE
        c.id = ?
        AND fr.year = (
            SELECT MAX(year)
            FROM financial_ratios f2
            WHERE f2.company_id = c.id
        )
    """

    df = pd.read_sql(query, conn, params=[ticker.upper()])

    conn.close()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return df.fillna("").iloc[0].to_dict()


# ======================================================
# PROFIT & LOSS
# ======================================================
@router.get("/companies/{ticker}/pl")
def get_profit_and_loss(
    ticker: str,
    from_year: int | None = Query(None),
    to_year: int | None = Query(None),
):

    conn = get_connection()

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
      AND year IS NOT NULL
    """

    params = [ticker.upper()]

    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year DESC"

    df = pd.read_sql(query, conn, params=params)

    conn.close()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No Profit & Loss data found"
        )

    return df.fillna("").to_dict(orient="records")

@router.get("/companies/{ticker}/bs")
def get_balance_sheet(
    ticker: str,
    from_year: int | None = Query(None),
    to_year: int | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id = ?
      AND year IS NOT NULL
    """

    params = [ticker.upper()]

    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year DESC"

    df = pd.read_sql(query, conn, params=params)

    conn.close()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No Balance Sheet data found"
        )

    return df.fillna("").to_dict(orient="records")

# ======================================================
# CASH FLOW
# ======================================================
@router.get("/companies/{ticker}/cashflow")
def get_cash_flow(
    ticker: str,
    from_year: int | None = Query(None),
    to_year: int | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id = ?
      AND year IS NOT NULL
    """

    params = [ticker.upper()]

    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)

    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year DESC"

    df = pd.read_sql(query, conn, params=params)

    conn.close()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No Cash Flow data found"
        )

    return df.fillna("").to_dict(orient="records")