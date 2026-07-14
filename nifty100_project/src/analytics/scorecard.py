import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

df.to_sql(
    "scorecard",
    conn,
    if_exists="replace",
    index=False
)

print("Scorecard rows:", len(df))

conn.close()