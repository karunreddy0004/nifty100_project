import sqlite3
import pandas as pd
import os

DB = "db/nifty100.db"
OUTPUT = "output/peer_comparison.xlsx"


def load_data():
    conn = sqlite3.connect(DB)

    peer = pd.read_sql(
        "SELECT * FROM peer_percentiles",
        conn
    )

    groups = pd.read_sql(
        "SELECT * FROM peer_groups",
        conn
    )

    companies = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """,
        conn
    )

    conn.close()

    return peer, groups, companies

def main():

    print("Loading data...")

    peer, groups, companies = load_data()

    os.makedirs("output", exist_ok=True)

    writer = pd.ExcelWriter(
        OUTPUT,
        engine="openpyxl"
    )

    peer_groups = sorted(groups["peer_group_name"].unique())

    print("Peer Groups Found:")
    print(peer_groups)

    for group in peer_groups:

        print(f"Creating sheet: {group}")

        company_ids = groups.loc[
            groups["peer_group_name"] == group,
            "company_id"
        ]

        sheet = peer[
            peer["company_id"].isin(company_ids)
        ].copy()

        # Convert metric rows into columns
        sheet = sheet.pivot_table(
            index=["company_id", "year"],
            columns="metric",
            values="percentile_rank"
        ).reset_index()

        # Add company names
        sheet = sheet.merge(
            companies,
            on="company_id",
            how="left"
        )

        # Write one sheet
        sheet.to_excel(
            writer,
            sheet_name=group[:31],
            index=False
        )

    writer.close()

    print()
    print("Excel report created successfully.")
    print(OUTPUT)

if __name__ == "__main__":
    main()