from fastapi import APIRouter
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
def dashboard():

    conn = get_connection()

    companies = pd.read_sql(
        "SELECT COUNT(*) AS total FROM companies",
        conn
    )

    sectors = pd.read_sql(
        "SELECT COUNT(DISTINCT broad_sector) AS total FROM sectors",
        conn
    )

    strong_buy = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM investment_scores
        WHERE rating='Strong Buy'
        """,
        conn
    )

    buy = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM investment_scores
        WHERE rating='Buy'
        """,
        conn
    )

    valuation = pd.read_sql(
        """
        SELECT valuation,
               COUNT(*) AS companies
        FROM valuation_summary
        GROUP BY valuation
        """,
        conn
    )

    risk = pd.read_sql(
        """
        SELECT overall_risk,
               COUNT(*) AS companies
        FROM risk_analysis
        GROUP BY overall_risk
        """,
        conn
    )

    conn.close()

    return {
        "total_companies": int(companies.iloc[0]["total"]),
        "total_sectors": int(sectors.iloc[0]["total"]),
        "strong_buy": int(strong_buy.iloc[0]["total"]),
        "buy": int(buy.iloc[0]["total"]),
        "valuation": valuation.to_dict(orient="records"),
        "risk": risk.to_dict(orient="records"),
    }