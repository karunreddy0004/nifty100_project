import sqlite3
import pandas as pd

from analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover
)

DB = "db/nifty100.db"


def run_ratios_engine():
    conn = sqlite3.connect(DB)

    pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
    bs = pd.read_sql("SELECT * FROM balancesheet", conn)
    cf = pd.read_sql("SELECT * FROM cashflow", conn)

    merged = pnl.merge(bs, on=["company_id", "year"], how="left") \
            .merge(cf, on=["company_id", "year"], how="left")

    merged = merged.drop_duplicates(subset=["company_id", "year"])

    results = []

    for _, r in merged.iterrows():

        net_profit = r["net_profit"]
        sales = r["sales"]

        equity = r["equity_capital"]
        reserves = r["reserves"]
        borrowings = r["borrowings"]

        ebit = r.get("ebit", 0)
        operating_profit = r.get("operating_profit", 0)
        other_income = r.get("other_income", 0)
        interest = r.get("interest", 0)
        total_assets = r.get("total_assets", 0)

        row = {
            "company_id": r["company_id"],
            "year": r["year"],

            "net_profit_margin_pct": net_profit_margin(net_profit, sales),
            "operating_profit_margin_pct": operating_profit_margin(operating_profit, sales),

            "return_on_equity_pct": return_on_equity(net_profit, equity, reserves),

            "debt_to_equity": debt_to_equity(borrowings, equity, reserves),

            "interest_coverage": interest_coverage_ratio(
                operating_profit, other_income, interest
            ),

            "asset_turnover": asset_turnover(sales, total_assets),

            "return_on_assets_pct": return_on_assets(net_profit, total_assets),

            "return_on_capital_employed_pct": return_on_capital_employed(
                ebit, equity, reserves, borrowings
            )
        }

        results.append(row)

        df = pd.DataFrame(results)
        df.to_sql("financial_ratios", conn, if_exists="replace", index=False)
        conn.close()
        print("financial_ratios populated:", len(df))


        if __name__ == "__main__":
            run_ratios_engine()