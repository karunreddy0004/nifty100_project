import sqlite3
from pathlib import Path

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import zscore


DB_PATH = Path(__file__).resolve().parents[2] / "db" / "nifty100.db"

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"

REPORT_DIR = Path(__file__).resolve().parents[2] / "reports"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_latest_data():

    conn = get_connection()

    query = """
    SELECT
        fr.*,
        s.broad_sector
    FROM financial_ratios fr

    LEFT JOIN sectors s
    ON fr.company_id = s.company_id

    WHERE fr.year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df



def load_clusters():

    path = OUTPUT_DIR / "cluster_labels.csv"

    return pd.read_csv(path)



def cluster_profile(df, clusters):

    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow",
        "operating_profit_margin_pct"
    ]


    merged = df.merge(
        clusters,
        on="company_id",
        how="inner"
    )


    profile = merged.groupby(
        [
            "cluster_id",
            "cluster_name"
        ]
    )[features].agg(
        [
            "mean",
            "median"
        ]
    )


    profile.columns = [
        "_".join(col)
        for col in profile.columns
    ]


    profile.reset_index(
        inplace=True
    )


    profile.to_csv(
        OUTPUT_DIR / "cluster_profile.csv",
        index=False
    )


    print(
        "Cluster profile created"
    )



def correlation_heatmap(df):

    features = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "free_cash_flow",
        "asset_turnover"
    ]


    corr = df[features].corr()


    plt.figure(
        figsize=(10,8)
    )


    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm"
    )


    plt.title(
        "Financial KPI Correlation Heatmap"
    )


    plt.savefig(
        REPORT_DIR / "correlation_heatmap.png",
        bbox_inches="tight"
    )


    plt.close()


    print(
        "Correlation heatmap created"
    )



def detect_outliers(df):

    metrics = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow",
        "operating_profit_margin_pct"
    ]


    result = []


    for sector, group in df.groupby(
        "broad_sector"
    ):

        temp = group.copy()


        for col in metrics:

            if col in temp.columns:

                temp[col+"_z"] = zscore(
                    temp[col].fillna(
                        temp[col].median()
                    )
                )


        for _, row in temp.iterrows():

            for col in metrics:

                z_col = col+"_z"

                if (
                    z_col in row
                    and abs(row[z_col]) > 3
                ):

                    result.append(
                        {
                            "company_id": row["company_id"],
                            "sector": sector,
                            "metric": col,
                            "z_score": row[z_col]
                        }
                    )


    outliers = pd.DataFrame(result)


    outliers.to_csv(
        OUTPUT_DIR / "outlier_report.csv",
        index=False
    )


    print(
        "Outlier report created:",
        len(outliers)
    )



def portfolio_statistics(df):

    metrics = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "free_cash_flow"
    ]


    stats = []


    for col in metrics:

        if col in df.columns:

            series = df[col].dropna()


            stats.append(
                {
                    "metric": col,
                    "P10": np.percentile(series,10),
                    "P25": np.percentile(series,25),
                    "P50": np.percentile(series,50),
                    "P75": np.percentile(series,75),
                    "P90": np.percentile(series,90),
                    "Mean": series.mean(),
                    "Std": series.std()
                }
            )


    pd.DataFrame(stats).to_csv(
        OUTPUT_DIR / "portfolio_stats.csv",
        index=False
    )


    print(
        "Portfolio statistics created"
    )



def run():

    print(
        "Loading financial data..."
    )

    df = load_latest_data()


    clusters = load_clusters()


    print(
        "Companies:",
        len(df)
    )


    cluster_profile(
        df,
        clusters
    )


    correlation_heatmap(
        df
    )


    detect_outliers(
        df
    )


    portfolio_statistics(
        df
    )


    print(
        "Day 37 completed"
    )



if __name__ == "__main__":

    run()