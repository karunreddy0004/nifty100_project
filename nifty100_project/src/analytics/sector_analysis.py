import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

query = """
SELECT
    s.sector,
    COUNT(*) AS companies,
    AVG(r.return_on_equity_pct) AS avg_roe,
    AVG(r.net_profit_margin_pct) AS avg_margin
FROM sectors s
JOIN financial_ratios r
ON s.company_id = r.company_id
GROUP BY s.sector
ORDER BY avg_roe DESC
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()