import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

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