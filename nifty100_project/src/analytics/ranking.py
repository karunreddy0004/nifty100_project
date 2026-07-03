import sqlite3
import pandas as pd

DB = "db/nifty100.db"


def create_rankings():
    conn = sqlite3.connect(DB)

    df = pd.read_sql("SELECT * FROM scorecard", conn)

    df["quality_score"] = (
        df["return_on_equity_pct"].fillna(0)
        + df["return_on_assets_pct"].fillna(0)
        + df["net_profit_margin_pct"].fillna(0)
    )

    df["quality_rank"] = (
        df.groupby("year")["quality_score"]
        .rank(ascending=False, method="dense")
    )

    df.to_sql(
        "rankings",
        conn,
        if_exists="replace",
        index=False
    )

    print("Rankings created:", len(df))

    conn.close()


if __name__ == "__main__":
    create_rankings()