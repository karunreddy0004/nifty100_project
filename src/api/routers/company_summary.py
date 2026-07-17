from fastapi import APIRouter, Query
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Company Summary"])


@router.get("/company-summary")
def get_company_summary(
    company_id: str | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT *
    FROM company_summary
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

    df = df.sort_values(
        by="company_id"
    )

    return df.fillna("").to_dict(orient="records")