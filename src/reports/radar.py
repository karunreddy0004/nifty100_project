import sqlite3
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import os

DB = "db/nifty100.db"

OUTPUT = "reports/radar_charts"


def load_data():

    conn = sqlite3.connect(DB)

    query = """

    SELECT

        fr.company_id,
        fr.year,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.free_cash_flow,

        

        pg.peer_group_name

    FROM financial_ratios fr

    LEFT JOIN peer_groups pg

    ON fr.company_id = pg.company_id

    """

    df = pd.read_sql(query, conn)

    conn.close()

    # Keep only the latest year for each company
    df = df.sort_values(["company_id", "year"])

    df = (
        df.groupby("company_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )


    # Composite score calculation

    df["composite_quality_score"] = (

        df["return_on_equity_pct"].fillna(0)

        +

        df["return_on_capital_employed_pct"].fillna(0)

        +

        df["net_profit_margin_pct"].fillna(0)

        -

        (df["debt_to_equity"].fillna(0) * 10)

    )


    return df



def create_radar(company):


    metrics = [

        
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "Composite"


    ]


    values = [
    company["return_on_equity_pct"],
    company["return_on_capital_employed_pct"],
    company["net_profit_margin_pct"],
    -company["debt_to_equity"],
    company["free_cash_flow"],
    company["composite_quality_score"]
]


    values = [

        0 if pd.isna(x) else x

        for x in values

    ]


    values.append(values[0])


    angles = np.linspace(

        0,

        2*np.pi,

        len(metrics)+1

    )


    fig, ax = plt.subplots(

        figsize=(7,7),

        subplot_kw=dict(
            polar=True
        )

    )


    ax.plot(

        angles,

        values

    )


    ax.fill(

        angles,

        values,

        alpha=0.25

    )


    ax.set_xticks(

        angles[:-1]

    )


    ax.set_xticklabels(

        metrics,

        fontsize=8

    )


    title = company["company_id"]


    if pd.notna(company["peer_group_name"]):

        title += "\n" + company["peer_group_name"]


    ax.set_title(

        title,

        size=12

    )


    filename = os.path.join(

        OUTPUT,

        str(company["company_id"])

        +

        "_radar.png"

    )


    plt.savefig(

        filename,

        bbox_inches="tight"

    )


    plt.close()



def main():


    os.makedirs(

        OUTPUT,

        exist_ok=True

    )


    print("Loading radar data...")


    df = load_data()


    print(

        "Companies loaded:",
        

        len(df)

    )


    print(

        "Generating radar charts..."

    )


    count = 0


    for _, company in df.iterrows():

        create_radar(company)

        count += 1


    print(

        "Radar charts created:",

        count

    )



if __name__ == "__main__":

    main()