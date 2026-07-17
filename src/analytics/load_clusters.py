import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def load_clusters():

    print("Loading cluster labels...")

    df = pd.read_csv(
        "output/cluster_labels.csv"
    )

    print("Rows:", len(df))


    conn = sqlite3.connect(DB_PATH)


    df.to_sql(
        "company_clusters",
        conn,
        if_exists="replace",
        index=False
    )


    conn.close()

    print("company_clusters table created.")


if __name__ == "__main__":
    load_clusters()