import sqlite3
import pandas as pd

DB = "db/nifty100.db"


def sector_analysis():

    conn = sqlite3.connect(DB)

    query = """
    SELECT
        s.broad_sector,
        COUNT(*) AS companies,
        AVG(r.return_on_equity_pct) AS avg_roe,
        AVG(r.net_profit_margin_pct) AS avg_margin
    FROM sectors s
    JOIN financial_ratios r
    ON s.company_id = r.company_id
    GROUP BY s.broad_sector
    ORDER BY avg_roe DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print(df)

    return df


if __name__ == "__main__":
    sector_analysis()