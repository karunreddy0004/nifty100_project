import sqlite3
import pandas as pd
import os

DB = "db/nifty100.db"


def sign(value):
    if pd.isna(value):
        return "0"
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "0"


def classify(cfo, cfi, cff, cfo_quality=None):
    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):
        if cfo_quality is not None and cfo_quality > 1:
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Other"


def generate_capital_allocation():

    conn = sqlite3.connect(DB)

    df = pd.read_sql("""
        SELECT
            p.company_id,
            p.year,
            p.net_profit,
            c.operating_activity,
            c.investing_activity,
            c.financing_activity
        FROM profitandloss p
        JOIN cashflow c
        ON p.company_id=c.company_id
        AND p.year=c.year
    """, conn)

    output = []

    for _, r in df.iterrows():

        cfo = sign(r["operating_activity"])
        cfi = sign(r["investing_activity"])
        cff = sign(r["financing_activity"])

        quality = None
        if r["net_profit"] != 0:
            quality = r["operating_activity"] / r["net_profit"]

        output.append({
            "company_id": r["company_id"],
            "year": r["year"],
            "cfo_sign": cfo,
            "cfi_sign": cfi,
            "cff_sign": cff,
            "pattern_label": classify(cfo, cfi, cff, quality)
        })

    os.makedirs("output", exist_ok=True)

    result = pd.DataFrame(output)

    result.to_csv("output/capital_allocation.csv", index=False)

    print("Capital allocation rows:", len(result))

    conn.close()


if __name__ == "__main__":
    generate_capital_allocation()