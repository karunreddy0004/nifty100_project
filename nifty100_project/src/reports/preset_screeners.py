import sqlite3
import pandas as pd

DB = "db/nifty100.db"

print("Loading data...")

conn = sqlite3.connect(DB)

query = """
SELECT
    company_id,
    year,
    net_profit_margin_pct,
    operating_profit_margin_pct,
    return_on_equity_pct,
    return_on_capital_employed_pct,
    debt_to_equity,
    return_on_assets_pct
FROM financial_ratios
"""

df = pd.read_sql(query, conn)
conn.close()

# Use latest year for each company
df = df.sort_values("year").groupby("company_id").tail(1)

print("Companies:", len(df))

screeners = {}

# Buffett Style
screeners["Buffett Style"] = df[
    (df["return_on_equity_pct"] >= 0.15) &
    (df["debt_to_equity"] <= 0.5)
]

# Quality Compounders
screeners["Quality Compounders"] = df[
    (df["return_on_equity_pct"] >= 0.18) &
    (df["return_on_capital_employed_pct"] >= 0.18)
]

# High Margin
screeners["High Margin"] = df[
    (df["net_profit_margin_pct"] >= 0.15) &
    (df["operating_profit_margin_pct"] >= 0.20)
]

# Asset Efficient
screeners["Asset Efficient"] = df[
    df["return_on_assets_pct"] >= 0.10
]

output = "output/preset_screeners.xlsx"

with pd.ExcelWriter(output, engine="openpyxl") as writer:
    for name, data in screeners.items():
        data.sort_values(
            "return_on_equity_pct",
            ascending=False
        ).to_excel(writer, sheet_name=name, index=False)

print(f"\nSaved to {output}")

for name, data in screeners.items():
    print(f"{name}: {len(data)} companies")