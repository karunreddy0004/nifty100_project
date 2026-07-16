import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


def load_pros_cons():

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql(
        "SELECT * FROM pros_cons ORDER BY company_id",
        conn,
    )

    conn.close()

    return df
def generate_summary(df):

    summaries = []

    companies = df["company_id"].unique()

    for company in companies:

        company_df = df[df["company_id"] == company]

        pros = company_df[company_df["type"] == "Pro"]
        cons = company_df[company_df["type"] == "Con"]

        pros_count = len(pros)
        cons_count = len(cons)

        if pros_count >= 5 and cons_count == 0:
            summary = (
                "The company demonstrates excellent financial strength with "
                "strong profitability, cash generation and operational efficiency."
            )

        elif pros_count > cons_count:
            summary = (
                "The company shows healthy financial performance with more "
                "strengths than weaknesses."
            )

        elif cons_count > pros_count:
            summary = (
                "The company exhibits multiple financial weaknesses that "
                "require careful evaluation."
            )

        else:
            summary = (
                "The company has a balanced financial profile with both "
                "strengths and weaknesses."
            )

        summaries.append({
            "company_id": company,
            "pros_count": pros_count,
            "cons_count": cons_count,
            "summary": summary,
        })

    return pd.DataFrame(summaries)

def save_output(df):

    conn = sqlite3.connect(DB_FILE)

    df.to_sql(
        "company_summary",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()

    output_file = OUTPUT_DIR / "company_summary.csv"

    df.to_csv(output_file, index=False)

    print()
    print("Saved to SQLite table : company_summary")
    print("CSV Saved :", output_file)

if __name__ == "__main__":

    pros_cons = load_pros_cons()

    print("Pros/Cons Loaded :", len(pros_cons))

    summary_df = generate_summary(pros_cons)

    print("Summaries Generated :", len(summary_df))

    save_output(summary_df)