from fastapi import APIRouter
import pandas as pd

from src.api.database import get_connection

router = APIRouter(tags=["Sectors"])


# ======================================================
# ALL SECTORS
# ======================================================
@router.get("/sectors")
def get_sectors():

    conn = get_connection()

    query = """
    SELECT
        broad_sector,
        COUNT(company_id) AS companies,
        AVG(index_weight_pct) AS avg_index_weight
    FROM sectors
    GROUP BY broad_sector
    ORDER BY broad_sector
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df.fillna("").to_dict(orient="records")


# ======================================================
# COMPANIES IN A SECTOR
# ======================================================
@router.get("/sectors/{sector_name}")
def get_sector_companies(sector_name: str):

    conn = get_connection()

    query = """
    SELECT
        s.company_id,
        c.company_name,
        s.sub_sector,
        s.market_cap_category,
        s.index_weight_pct
    FROM sectors s

    LEFT JOIN companies c
        ON s.company_id = c.id

    WHERE LOWER(s.broad_sector) = LOWER(?)

    ORDER BY c.company_name
    """

    df = pd.read_sql(
        query,
        conn,
        params=[sector_name]
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")