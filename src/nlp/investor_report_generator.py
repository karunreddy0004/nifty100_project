import sqlite3
import pandas as pd
from pathlib import Path


# ---------------------------------------------
# Paths
# ---------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT_PATH = BASE_DIR / "output" / "investor_reports.xlsx"



# ---------------------------------------------
# Connection
# ---------------------------------------------

def get_connection():

    return sqlite3.connect(DB_PATH)



# ---------------------------------------------
# Generate Report
# ---------------------------------------------

def generate_report(row):

    report = f"""
Company: {row['company_id']}


Investment Rating:
{row['rating']}


Final Investment Score:
{row['final_score']}/100


Quality Score:
{row['quality_score']}


Growth Score:
{row['growth_score']}


Valuation Score:
{row['valuation_score']}


Risk Score:
{row['risk_score']}


Investment View:

This company is evaluated based on:
- Financial quality
- Growth potential
- Valuation
- Risk parameters


Overall Assessment:

"""

    if row["rating"] == "Strong Buy":

        report += (
            "Company shows strong fundamentals "
            "with attractive investment characteristics."
        )

    elif row["rating"] == "Buy":

        report += (
            "Company demonstrates positive "
            "long term investment potential."
        )

    elif row["rating"] == "Hold":

        report += (
            "Company requires further monitoring "
            "before investment decision."
        )

    else:

        report += (
            "Company carries higher risk "
            "and requires caution."
        )


    return report



# ---------------------------------------------
# Main
# ---------------------------------------------

def main():

    conn = get_connection()


    print("Loading investment scores...")


    scores = pd.read_sql(
        """
        SELECT *
        FROM investment_scores
        """,
        conn
    )


    conn.close()



    print(
        "Generating investor reports..."
    )


    scores["investor_report"] = scores.apply(
        generate_report,
        axis=1
    )


    scores.to_excel(
        OUTPUT_PATH,
        index=False
    )


    print(
        "Reports Generated:",
        len(scores)
    )


    print(
        "Saved:",
        OUTPUT_PATH
    )



if __name__ == "__main__":

    main()