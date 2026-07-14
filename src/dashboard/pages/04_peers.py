import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "peer_groups",
    "market_cap",
    "stock_prices",
    "balancesheet",
    "cashflow",
    "documents",
    "peer_percentiles",
    "scorecard"
]

for table in tables:
    print("\n" + "=" * 60)
    print(table.upper())
    print("=" * 60)

    try:
        print(pd.read_sql(f"PRAGMA table_info({table})", conn))
        print("\nSample Data:")
        print(pd.read_sql(f"SELECT * FROM {table} LIMIT 3", conn))
    except Exception as e:
        print(e)

conn.close()