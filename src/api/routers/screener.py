from fastapi import APIRouter, Query
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Screener"])


@router.get("/screener")
def screener(
    min_roe: float | None = Query(None),
    min_roce: float | None = Query(None),
    sector: str | None = Query(None),
    market_cap: str | None = Query(None),
):

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.market_cap_category,
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.revenue_cagr_5yr

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

    print("\n========== BEFORE FILTER ==========")
    print("Rows:", len(df))
    print(df.head())

    print("\nParameters")
    print("min_roe =", min_roe)
    print("min_roce =", min_roce)
    print("sector =", sector)
    print("market_cap =", market_cap)

    # Clean strings
    df["broad_sector"] = (
        df["broad_sector"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["market_cap_category"] = (
        df["market_cap_category"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Convert numeric columns
    numeric_cols = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if min_roe is not None:
        df = df[df["return_on_equity_pct"] >= min_roe]
        print("After ROE filter:", len(df))

    if min_roce is not None:
        df = df[df["return_on_capital_employed_pct"] >= min_roce]
        print("After ROCE filter:", len(df))

    if sector:
        df = df[
            df["broad_sector"].str.lower()
            == sector.strip().lower()
        ]
        print("After Sector filter:", len(df))

    if market_cap:
        market_cap = " ".join(market_cap.split())

    df = df[
        df["market_cap_category"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.lower()
        == market_cap.lower()
    ]

    df = df[
        df["market_cap_category"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.lower()
        == market_cap.lower()
    ]

    df = df.sort_values(
        by="return_on_equity_pct",
        ascending=False
    )

    print("Final Rows:", len(df))
    print("===============================\n")

    return df.fillna("").to_dict(orient="records")