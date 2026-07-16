import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "db" / "nifty100.db"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "output"

OUTPUT_PATH.mkdir(exist_ok=True)

def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        r.company_id,
        r.year,
        r.return_on_equity_pct,
        r.return_on_capital_employed_pct,
        r.net_profit_margin_pct,
        r.debt_to_equity,
        c.company_name
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


def valuation_label(row):

    score = 0

    if row["return_on_equity_pct"] >= 20:
        score += 1

    if row["return_on_capital_employed_pct"] >= 20:
        score += 1

    if row["net_profit_margin_pct"] >= 15:
        score += 1

    if row["debt_to_equity"] <= 0.5:
        score += 1


    if score >= 4:
        return "Undervalued"

    elif score >= 2:
        return "Fairly Valued"

    return "Overvalued"



def main():

    print("Loading financial ratios...")

    df = load_data()


    # Create valuation category
    df["valuation"] = df.apply(
        valuation_label,
        axis=1
    )


    # Create valuation flags

    df["High ROE"] = (
        df["return_on_equity_pct"] >= 20
    )

    df["High ROCE"] = (
        df["return_on_capital_employed_pct"] >= 20
    )

    df["Healthy Margin"] = (
        df["net_profit_margin_pct"] >= 15
    )

    df["Low Debt"] = (
        df["debt_to_equity"] <= 0.5
    )


    flags = df[
        [
            "company_id",
            "company_name",
            "High ROE",
            "High ROCE",
            "Healthy Margin",
            "Low Debt",
            "valuation",
        ]
    ]


    flags.to_csv(
        OUTPUT_PATH / "valuation_flags.csv",
        index=False
    )


    output_file = OUTPUT_PATH / "valuation_summary.xlsx"


    df.to_excel(
        output_file,
        index=False
    )


    print("Valuation summary created.")

    print(
        df["valuation"].value_counts()
    )


if __name__ == "__main__":
    main()