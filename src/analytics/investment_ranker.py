import sqlite3
import pandas as pd
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "db" / "nifty100.db"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "output"


def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        r.company_id,
        c.company_name,
        r.return_on_equity_pct,
        r.return_on_capital_employed_pct,
        r.net_profit_margin_pct,
        r.debt_to_equity
    FROM financial_ratios r
    JOIN companies c
        ON r.company_id = c.id
    WHERE r.year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df



def calculate_score(row):

    score = 0


    # ROE (25 points)
    if row["return_on_equity_pct"] >= 20:
        score += 25
    elif row["return_on_equity_pct"] >= 10:
        score += 15


    # ROCE (25 points)
    if row["return_on_capital_employed_pct"] >= 20:
        score += 25
    elif row["return_on_capital_employed_pct"] >= 10:
        score += 15


    # Profit Margin (15 points)
    if row["net_profit_margin_pct"] >= 15:
        score += 15
    elif row["net_profit_margin_pct"] >= 8:
        score += 8


    # Debt (15 points)
    if row["debt_to_equity"] <= 0.5:
        score += 15
    elif row["debt_to_equity"] <= 1:
        score += 8


    return score



def get_recommendation(score):

    if score >= 70:
        return "BUY"

    elif score >= 45:
        return "HOLD"

    else:
        return "AVOID"



def main():

    print("Loading company fundamentals...")

    df = load_data()


    print("Calculating investment score...")


    df["investment_score"] = df.apply(
        calculate_score,
        axis=1
    )


    df["recommendation"] = df["investment_score"].apply(
        get_recommendation
    )


    df = df.sort_values(
        by="investment_score",
        ascending=False
    )


    output_file = OUTPUT_PATH / "investment_ranking.xlsx"


    df.to_excel(
        output_file,
        index=False
    )


    print("Investment ranking created.")

    print(
        df[
            [
                "company_name",
                "investment_score",
                "recommendation"
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()