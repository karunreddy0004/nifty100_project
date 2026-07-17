from fastapi import APIRouter, Query
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Stock Prices"])


@router.get("/stock-prices")
def get_stock_prices(
    company_id: str | None = Query(None),
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT *
    FROM stock_prices
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if company_id:
        df = df[
            df["company_id"]
            .fillna("")
            .str.upper()
            ==
            company_id.strip().upper()
        ]

    if from_date:
        df = df[df["date"] >= from_date]

    if to_date:
        df = df[df["date"] <= to_date]

    df = df.sort_values(
        by="date",
        ascending=False
    )

    return df.fillna("").to_dict(orient="records")