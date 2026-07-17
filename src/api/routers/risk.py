from fastapi import APIRouter, Query
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Risk Analysis"])


@router.get("/risk")
def get_risk_analysis(
    overall_risk: str | None = Query(None),
    debt_risk: str | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT
        r.company_id,
        c.company_name,
        r.debt_risk,
        r.profit_risk,
        r.cashflow_risk,
        r.overall_risk,
        r.risk_score

    FROM risk_analysis r

    LEFT JOIN companies c
        ON r.company_id = c.id

    ORDER BY r.risk_score ASC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if overall_risk:
        df = df[
            df["overall_risk"]
            .fillna("")
            .str.strip()
            .str.lower()
            ==
            overall_risk.strip().lower()
        ]

    if debt_risk:
        df = df[
            df["debt_risk"]
            .fillna("")
            .str.strip()
            .str.lower()
            ==
            debt_risk.strip().lower()
        ]

    return df.fillna("").to_dict(orient="records")