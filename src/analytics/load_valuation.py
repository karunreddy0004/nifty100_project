import sqlite3
import pandas as pd

# Load Excel
df = pd.read_excel("output/valuation_summary.xlsx")

# Connect database
conn = sqlite3.connect("db/nifty100.db")

# Save table
df.to_sql(
    "valuation_summary",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("valuation_summary table created successfully!")
print(df.head())