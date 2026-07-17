from fastapi import APIRouter, HTTPException
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Documents"])


@router.get("/companies/{ticker}/documents")
def get_documents(ticker: str):

    conn = get_connection()

    query = """
    SELECT *
    FROM documents
    WHERE company_id = ?
    ORDER BY year DESC
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker.upper()]
    )

    conn.close()

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="No documents found"
        )

    return df.fillna("").to_dict(orient="records")