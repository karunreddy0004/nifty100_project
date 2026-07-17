import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
EXCEL_PATH = BASE_DIR / "output" / "investment_scores.xlsx"

# Load Excel
df = pd.read_excel(EXCEL_PATH)

# Connect database
conn = sqlite3.connect(DB_PATH)

# Save to SQLite
df.to_sql(
    "investment_scores",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("investment_scores table created successfully!")
print(df.head())