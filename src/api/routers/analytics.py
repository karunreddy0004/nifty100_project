from fastapi import APIRouter
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Analytics"])


@router.get("/analytics")
def analytics():

    conn = get_connection()

    company_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM companies",
        conn
    ).iloc[0]["total"]

    sector_count = pd.read_sql(
        """
        SELECT COUNT(DISTINCT broad_sector) AS total
        FROM sectors
        """,
        conn
    ).iloc[0]["total"]

    valuation = pd.read_sql(
        """
        SELECT valuation,
               COUNT(*) AS companies
        FROM valuation_summary
        GROUP BY valuation
        """,
        conn
    )

    ratings = pd.read_sql(
        """
        SELECT rating,
               COUNT(*) AS companies
        FROM investment_scores
        GROUP BY rating
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

    sectors = pd.read_sql(
        """
        SELECT broad_sector,
               COUNT(*) AS companies
        FROM sectors
        GROUP BY broad_sector
        ORDER BY companies DESC
        """,
        conn
    )

    conn.close()

    return {
        "total_companies": int(company_count),
        "total_sectors": int(sector_count),
        "valuation_summary": valuation.to_dict(orient="records"),
        "investment_ratings": ratings.to_dict(orient="records"),
        "risk_summary": risk.to_dict(orient="records"),
        "sector_distribution": sectors.to_dict(orient="records"),
    }