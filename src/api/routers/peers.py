from fastapi import APIRouter, HTTPException
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Peers"])


# ======================================================
# GET PEERS OF A COMPANY
# ======================================================
@router.get("/peers/{ticker}")
def get_company_peers(ticker: str):

    conn = get_connection()

    # Find the peer group for this company
    group_df = pd.read_sql(
        """
        SELECT peer_group_name
        FROM peer_groups
        WHERE company_id = ?
        """,
        conn,
        params=[ticker.upper()],
    )

    if group_df.empty:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Peer group not found"
        )

    peer_group = group_df.iloc[0]["peer_group_name"]

    query = """
    SELECT
        pg.company_id,
        c.company_name,
        pg.peer_group_name,
        pg.is_benchmark
    FROM peer_groups pg
    LEFT JOIN companies c
        ON pg.company_id = c.id
    WHERE pg.peer_group_name = ?
    ORDER BY pg.is_benchmark DESC, c.company_name
    """

    df = pd.read_sql(query, conn, params=[peer_group])

    conn.close()

    return df.fillna("").to_dict(orient="records")


# ======================================================
# GET PERCENTILES OF A COMPANY
# ======================================================
@router.get("/peers/{ticker}/percentiles")
def get_company_percentiles(ticker: str):

    conn = get_connection()

    query = """
    SELECT
        peer_group_name,
        metric,
        value,
        percentile_rank,
        year
    FROM peer_percentiles
    WHERE company_id = ?
    ORDER BY metric
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
            detail="No percentile data found"
        )

    return df.fillna("").to_dict(orient="records")