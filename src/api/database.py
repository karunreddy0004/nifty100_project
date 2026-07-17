from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

print("DATABASE =", DB_PATH)


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_db_row_counts():
    tables = [
        "companies",
        "financial_ratios",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "rankings",
        "valuation_summary",
        "pros_cons",
        "company_summary",
        "stock_prices",
    ]

    conn = get_connection()
    cursor = conn.cursor()

    counts = {}

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        except Exception:
            counts[table] = 0

    conn.close()

    return counts