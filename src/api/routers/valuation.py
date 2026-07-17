from fastapi import APIRouter, Query
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Valuation"])


@router.get("/valuation")
def valuation(
    valuation: str | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT *
    FROM valuation_summary
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if valuation:
        df = df[
            df["valuation"]
            .fillna("")
            .str.strip()
            .str.lower()
            ==
            valuation.strip().lower()
        ]

    return df.fillna("").to_dict(orient="records")
@router.get("/valuation")
def valuation(
    valuation: str | None = Query(None),
):
    conn = get_connection()

    df = pd.read_sql("SELECT * FROM valuation_summary", conn)
    conn.close()

    print("Rows loaded:", len(df))
    print(df.head())

    if valuation:
        print("Filter =", valuation)

        df = df[
            df["valuation"]
            .fillna("")
            .str.strip()
            .str.lower()
            ==
            valuation.strip().lower()
        ]

        print("Rows after filter:", len(df))

    return df.fillna("").to_dict(orient="records")