import sqlite3
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


DB_PATH = "db/nifty100.db"


def run_clustering():

    print("Loading financial data...")

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql("""
        SELECT
            company_id,
            year,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            return_on_equity_pct,
            return_on_capital_employed_pct,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr
        FROM financial_ratios
        WHERE year = 2024
    """, conn)


    print("Companies:", len(df))


    features = [
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr"
    ]


    # Handle missing values
    df[features] = df[features].fillna(
        df[features].median()
    )


    print("Scaling features...")

    scaler = StandardScaler()

    X = scaler.fit_transform(df[features])


    print("Running KMeans...")


    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=20
    )


    df["cluster_id"] = model.fit_predict(X)


    cluster_names = {
        0: "High Quality Compounders",
        1: "Defensive Companies",
        2: "Value Cyclicals",
        3: "Emerging Growth",
        4: "Turnaround / Risk"
    }


    df["cluster_name"] = df["cluster_id"].map(cluster_names)


    # Distance from cluster center
    distances = model.transform(X)

    df["distance_from_centroid"] = [
        distances[i][cluster]
        for i, cluster in enumerate(df["cluster_id"])
    ]


    output = df[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid"
        ]
    ]


    output.to_csv(
        "output/cluster_labels.csv",
        index=False
    )


    print("\nCluster Summary:")
    print(output["cluster_name"].value_counts())


    conn.close()


    print("\nSaved: output/cluster_labels.csv")


if __name__ == "__main__":
    run_clustering()