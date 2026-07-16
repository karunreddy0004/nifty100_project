import sqlite3
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
OUTPUT_PATH = BASE_DIR / "output" / "investment_scores.xlsx"


# --------------------------------------------------
# Database
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# Score Functions
# --------------------------------------------------

def calculate_quality_score(row):

    score = 0

    # ROE
    if pd.notna(row["return_on_equity_pct"]):
        if row["return_on_equity_pct"] > 20:
            score += 30
        elif row["return_on_equity_pct"] > 15:
            score += 20
        else:
            score += 10


    # ROCE
    if pd.notna(row["return_on_capital_employed_pct"]):
        if row["return_on_capital_employed_pct"] > 20:
            score += 30
        elif row["return_on_capital_employed_pct"] > 12:
            score += 20
        else:
            score += 10


    # Operating Margin
    if pd.notna(row["operating_profit_margin_pct"]):
        if row["operating_profit_margin_pct"] > 25:
            score += 20
        elif row["operating_profit_margin_pct"] > 15:
            score += 15
        else:
            score += 5


    # Cash Flow
    if pd.notna(row["free_cash_flow"]):
        if row["free_cash_flow"] > 0:
            score += 20


    return score



def calculate_growth_score(row):

    score = 0

    if pd.notna(row["revenue_cagr_5yr"]):

        if row["revenue_cagr_5yr"] > 15:
            score += 50

        elif row["revenue_cagr_5yr"] > 8:
            score += 30


    if pd.notna(row["pat_cagr_5yr"]):

        if row["pat_cagr_5yr"] > 20:
            score += 50

        elif row["pat_cagr_5yr"] > 10:
            score += 30


    return score



def calculate_risk_score(row):

    score = 100


    # Debt Risk
    if pd.notna(row["debt_to_equity"]):

        if row["debt_to_equity"] > 2:
            score -= 40

        elif row["debt_to_equity"] > 1:
            score -= 20


    # Interest Coverage

    if pd.notna(row["interest_coverage"]):

        if row["interest_coverage"] < 2:
            score -= 30


    return max(score,0)



def valuation_score(row):

    if row["valuation"] == "Fairly Valued":
        return 80

    elif row["valuation"] == "Undervalued":
        return 90

    else:
        return 50



# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    conn = get_connection()


    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE year = (
            SELECT MAX(year)
            FROM financial_ratios
        )
        """,
        conn
    )


    try:

        valuation = pd.read_sql(
            """
            SELECT company_id, valuation
            FROM valuation_summary
            """,
            conn
        )

        ratios = ratios.merge(
            valuation,
            on="company_id",
            how="left"
        )

    except:

        ratios["valuation"] = "Unknown"



    conn.close()


    print("Calculating investment scores...")


    ratios["quality_score"] = ratios.apply(
        calculate_quality_score,
        axis=1
    )


    ratios["growth_score"] = ratios.apply(
        calculate_growth_score,
        axis=1
    )


    ratios["risk_score"] = ratios.apply(
        calculate_risk_score,
        axis=1
    )


    ratios["valuation_score"] = ratios.apply(
        valuation_score,
        axis=1
    )


    ratios["final_score"] = (
        ratios["quality_score"] * 0.35 +
        ratios["growth_score"] * 0.25 +
        ratios["valuation_score"] * 0.20 +
        ratios["risk_score"] * 0.20
    ).round(2)



    def rating(score):

        if score >= 80:
            return "Strong Buy"

        elif score >= 65:
            return "Buy"

        elif score >= 50:
            return "Hold"

        else:
            return "Avoid"



    ratios["rating"] = ratios["final_score"].apply(rating)


    output = ratios[
        [
            "company_id",
            "quality_score",
            "growth_score",
            "valuation_score",
            "risk_score",
            "final_score",
            "rating"
        ]
    ].sort_values(
        "final_score",
        ascending=False
    )


    output.to_excel(
        OUTPUT_PATH,
        index=False
    )


    print(output.head(10))

    print("\nInvestment scores created:")
    print(OUTPUT_PATH)



if __name__ == "__main__":
    main()