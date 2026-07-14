import sqlite3
import pandas as pd

DB = "db/nifty100.db"


def company_report(company, year):
    conn = sqlite3.connect(DB)

    query = """
    SELECT
        r.company_id,
        r.year,
        p.sales,
        p.net_profit,
        r.net_profit_margin_pct,
        r.operating_profit_margin_pct,
        r.return_on_equity_pct,
        r.debt_to_equity,
        r.interest_coverage,
        rk.quality_score,
        rk.quality_rank
    FROM financial_ratios r
    JOIN profitandloss p
        ON r.company_id = p.company_id
       AND r.year = p.year
    JOIN rankings rk
        ON r.company_id = rk.company_id
       AND r.year = rk.year
    WHERE r.company_id = ?
      AND r.year = ?
    """

    df = pd.read_sql(query, conn, params=(company, year))

    conn.close()

    if df.empty:
        print("No data found.")
    else:
        print(df)


if __name__ == "__main__":
    company_report("BEL", 2024)