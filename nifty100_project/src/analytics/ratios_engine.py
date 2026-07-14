import sqlite3
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(__file__))

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
    free_cash_flow,
    cfo_pat_ratio,
)

DB = "db/nifty100.db"


def run_ratios_engine():

    conn = sqlite3.connect(DB)

    print("Loading financial data...")

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cf = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    merged = (
        pnl
        .merge(
            bs,
            on=["company_id", "year"],
            how="left"
        )
        .merge(
            cf,
            on=["company_id", "year"],
            how="left"
        )
    )

    merged = merged.drop_duplicates(
        subset=["company_id", "year"]
    )

    results = []

    print("Calculating ratios...")

    for _, r in merged.iterrows():

        net_profit = r["net_profit"]
        sales = r["sales"]

        operating_activity = r["operating_activity"]
        investing_activity = r["investing_activity"]

        equity_capital = r["equity_capital"]
        reserves = r["reserves"]
        borrowings = r["borrowings"]
        total_assets = r["total_assets"]

        operating_profit = r["operating_profit"]
        other_income = r["other_income"]
        interest = r["interest"]

        # Convert balance-sheet values
        equity_capital *= 100
        reserves *= 100
        borrowings *= 100
        total_assets *= 100

        ebit = operating_profit

        fcf = free_cash_flow(
            operating_activity,
            investing_activity
        )

        cfo_pat = cfo_pat_ratio(
            operating_activity,
            net_profit
        )

        row = {
            "company_id": r["company_id"],
            "year": r["year"],

            "net_profit_margin_pct":
                net_profit_margin(
                    net_profit,
                    sales
                ),

            "operating_profit_margin_pct":
                operating_profit_margin(
                    operating_profit,
                    sales
                ),

            "return_on_equity_pct":
                return_on_equity(
                    net_profit,
                    equity_capital,
                    reserves
                ),

            "debt_to_equity":
                debt_to_equity(
                    borrowings,
                    equity_capital,
                    reserves
                ),

            "interest_coverage":
                interest_coverage_ratio(
                    operating_profit,
                    other_income,
                    interest
                ),

            "asset_turnover":
                asset_turnover(
                    sales,
                    total_assets
                ),

            "return_on_assets_pct":
                return_on_assets(
                    net_profit,
                    total_assets
                ),

            "return_on_capital_employed_pct":
                return_on_capital_employed(
                    ebit,
                    equity_capital,
                    reserves,
                    borrowings
                ),

            "free_cash_flow": fcf,
            "cfo_pat_ratio": cfo_pat,
        }

        results.append(row)

    df = pd.DataFrame(results)

    print(df.head())

    print("\nColumn Types:")
    print(df.dtypes)

    print("\nChecking for dict values...")

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, dict)).any():
            print(f"Dictionary found in column: {col}")

    df.to_sql(
        "financial_ratios",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(
        "financial_ratios populated:",
        len(df)
    )


if __name__ == "__main__":
    run_ratios_engine()