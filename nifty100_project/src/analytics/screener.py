import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

df = pd.read_sql(
    """
    SELECT *
    FROM rankings
    """,
    conn
)

conn.close()

def screen_stocks(df):

    result = df[
        (df["quality_score"] > 50)
    ]

    return result
def screen_stocks(df):

    result = df[
        (df["quality_score"] > 50)
    ]

    return result
filtered = screen_stocks(df)

filtered = filtered.sort_values(
    "quality_score",
    ascending=False
)

print(filtered.head(20))

def screen_stocks(df):

    result = df[

        (df["quality_score"] > 50)

    ]

    return result
filtered.to_csv(
    "output/screener.csv",
    index=False
)

print("Stocks found:", len(filtered))