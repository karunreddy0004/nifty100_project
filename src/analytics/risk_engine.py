import sqlite3
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
OUTPUT_PATH = BASE_DIR / "output" / "risk_analysis.xlsx"


# --------------------------------------------------
# Database Connection
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# Risk Rules
# --------------------------------------------------

def debt_risk(row):

    de = row["debt_to_equity"]

    if pd.isna(de):
        return "Unknown"

    if de > 2:
        return "High Risk"

    elif de > 1:
        return "Medium Risk"

    else:
        return "Low Risk"



def profit_risk(row):

    pat = row["pat_cagr_5yr"]

    if pd.isna(pat):
        return "Unknown"

    if pat < 0:
        return "Profit Decline"

    elif pat < 10:
        return "Slow Growth"

    else:
        return "Healthy"



def cashflow_risk(row):

    fcf = row["free_cash_flow"]

    if pd.isna(fcf):
        return "Unknown"

    if fcf < 0:
        return "Warning"

    else:
        return "Healthy"



def calculate_risk_score(row):

    score = 100


    # Debt

    if row["debt_risk"] == "High Risk":
        score -= 40

    elif row["debt_risk"] == "Medium Risk":
        score -= 20


    # Profit

    if row["profit_risk"] == "Profit Decline":
        score -= 30

    elif row["profit_risk"] == "Slow Growth":
        score -= 10


    # Cash Flow

    if row["cashflow_risk"] == "Warning":
        score -= 20


    return max(score, 0)



def overall_risk(score):

    if score >= 80:
        return "Low Risk"

    elif score >= 50:
        return "Medium Risk"

    else:
        return "High Risk"



# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    conn = get_connection()


    print("Loading financial data...")


    df = pd.read_sql(
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


    conn.close()


    print("Calculating risk metrics...")


    df["debt_risk"] = df.apply(
        debt_risk,
        axis=1
    )


    df["profit_risk"] = df.apply(
        profit_risk,
        axis=1
    )


    df["cashflow_risk"] = df.apply(
        cashflow_risk,
        axis=1
    )


    df["risk_score"] = df.apply(
        calculate_risk_score,
        axis=1
    )


    df["overall_risk"] = df["risk_score"].apply(
        overall_risk
    )


    output = df[
        [
            "company_id",
            "debt_risk",
            "profit_risk",
            "cashflow_risk",
            "overall_risk",
            "risk_score"
        ]
    ].sort_values(
        "risk_score"
    )


    output.to_excel(
        OUTPUT_PATH,
        index=False
    )


    print(output.head(20))


    print("\nRisk analysis created:")
    print(OUTPUT_PATH)



if __name__ == "__main__":
    main()