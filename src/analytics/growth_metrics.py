import sqlite3
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(__file__))

from ratios import calculate_cagr


DB = "db/nifty100.db"


def calculate_growth_metrics():

    conn = sqlite3.connect(DB)

    print("Loading profit and loss data...")

    pnl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            net_profit,
            eps
        FROM profitandloss
        ORDER BY company_id, year
        """,
        conn
    )


    results = []


    print("Calculating 5 year CAGR...")


    for company, group in pnl.groupby("company_id"):

        group = group.sort_values("year")


        for _, row in group.iterrows():

            current_year = row["year"]


            previous = group[
                group["year"] == current_year - 5
            ]


            if len(previous) == 1:

                old = previous.iloc[0]


                revenue_cagr, _ = calculate_cagr(
                    old["sales"],
                    row["sales"],
                    5
                )


                pat_cagr, _ = calculate_cagr(
                    old["net_profit"],
                    row["net_profit"],
                    5
                )


                eps_cagr, _ = calculate_cagr(
                    old["eps"],
                    row["eps"],
                    5
                )


                results.append({

                    "company_id": company,

                    "year": current_year,

                    "revenue_cagr_5yr": revenue_cagr,

                    "pat_cagr_5yr": pat_cagr,

                    "eps_cagr_5yr": eps_cagr

                })


    growth_df = pd.DataFrame(results)


    print(
        "Growth rows:",
        len(growth_df)
    )


    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )


    ratios = ratios.merge(
        growth_df,
        on=[
            "company_id",
            "year"
        ],
        how="left"
    )


    ratios.to_sql(
        "financial_ratios",
        conn,
        if_exists="replace",
        index=False
    )


    conn.close()


    print(
        "Growth metrics added successfully"
    )


if __name__ == "__main__":

    calculate_growth_metrics()
    