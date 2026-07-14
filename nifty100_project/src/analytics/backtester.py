import sqlite3
import pandas as pd

DB = "db/nifty100.db"


def run_backtest():

    conn = sqlite3.connect(DB)

    print("Loading rankings...")

    rankings = pd.read_sql("""
    SELECT company_id, quality_rank
    FROM rankings
    ORDER BY quality_rank
    LIMIT 10
    """, conn)

    print(rankings)

    print("\nLoading prices...")

    prices = pd.read_sql("""
    SELECT
        company_id,
        date,
        adjusted_close
    FROM stock_prices
    """, conn)

    conn.close()

    prices["date"] = pd.to_datetime(prices["date"])

    # Keep only top-ranked companies
    prices = prices[
        prices["company_id"].isin(rankings["company_id"])
    ]

    print("Price rows:", len(prices))

    # Pivot price table
    portfolio = prices.pivot(
        index="date",
        columns="company_id",
        values="adjusted_close"
    )

    # Monthly returns
    monthly_returns = portfolio.pct_change()

    # Equal-weight portfolio return
    portfolio_return = monthly_returns.mean(axis=1)

    # Remove first NaN
    portfolio_return = portfolio_return.dropna()

    # Cumulative return
    cumulative_return = (1 + portfolio_return).cumprod()

    # ----------------------------
    # Performance Metrics
    # ----------------------------

    total_return = cumulative_return.iloc[-1] - 1

    years = len(portfolio_return) / 12

    cagr = (cumulative_return.iloc[-1] ** (1 / years)) - 1

    volatility = portfolio_return.std() * (12 ** 0.5)

    if volatility != 0:
        sharpe = cagr / volatility
    else:
        sharpe = 0

    rolling_max = cumulative_return.cummax()

    drawdown = (
        cumulative_return - rolling_max
    ) / rolling_max

    max_drawdown = drawdown.min()

    # ----------------------------
    # Performance Data
    # ----------------------------

    result = pd.DataFrame({
        "Portfolio Return": portfolio_return,
        "Cumulative Return": cumulative_return,
        "Drawdown": drawdown
    })

    # ----------------------------
    # Summary Data
    # ----------------------------

    summary = pd.DataFrame({
        "Metric": [
            "Total Return",
            "CAGR",
            "Volatility",
            "Sharpe Ratio",
            "Maximum Drawdown"
        ],
        "Value": [
            total_return,
            cagr,
            volatility,
            sharpe,
            max_drawdown
        ]
    })

    # ----------------------------
    # Export
    # ----------------------------

    with pd.ExcelWriter(
        "output/backtest_results.xlsx",
        engine="openpyxl"
    ) as writer:

        result.to_excel(
            writer,
            sheet_name="Performance"
        )

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

    print("\n===== Portfolio Metrics =====")
    print(summary)

    print("\nBacktest completed.")
    print("\nExcel saved to output/backtest_results.xlsx")


if __name__ == "__main__":
    run_backtest()