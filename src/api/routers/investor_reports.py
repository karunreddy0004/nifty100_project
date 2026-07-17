from fastapi import APIRouter, Query
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Investor Reports"])


@router.get("/investor-reports")
def get_investor_reports(
    rating: str | None = Query(None),
    company_id: str | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT *
    FROM investor_reports
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if rating:
        df = df[
            df["rating"]
            .fillna("")
            .str.strip()
            .str.lower()
            ==
            rating.strip().lower()
        ]

    if company_id:
        df = df[
            df["company_id"]
            .fillna("")
            .str.upper()
            ==
            company_id.strip().upper()
        ]

    df = df.sort_values(
        by="final_score",
        ascending=False
    )

    return df.fillna("").to_dict(orient="records")