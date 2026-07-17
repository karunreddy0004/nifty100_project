from fastapi import APIRouter, Query
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Investment Scores"])


@router.get("/investment-scores")
def investment_scores(
    rating: str | None = Query(None),
    min_score: float | None = Query(None),
):
    conn = get_connection()

    query = """
    SELECT *
    FROM investment_scores
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if rating:
        df = df[
            df["rating"]
            .fillna("")
            .str.strip()
            .str.lower()
            == rating.strip().lower()
        ]

    if min_score is not None:
        df = df[df["final_score"] >= min_score]

    df = df.sort_values(
        by="final_score",
        ascending=False
    )

    return df.fillna("").to_dict(orient="records")