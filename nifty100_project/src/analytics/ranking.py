import sqlite3
import pandas as pd

DB = "db/nifty100.db"


def normalize(series):
    """
    Min-Max normalization
    Converts values between 0 and 100
    """

    series = pd.to_numeric(series, errors="coerce")

    # Fill missing values with median
    series = series.fillna(series.median())

    minimum = series.min()
    maximum = series.max()

    # If all values are the same
    if maximum == minimum:
        return pd.Series(50, index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100


def create_rankings():

    with sqlite3.connect(DB) as conn:

        print("Loading scorecard...")

        df = pd.read_sql(
            "SELECT * FROM scorecard",
            conn
        )

        print("Calculating normalized scores...")

        # -------------------------
        # Profitability Scores
        # -------------------------

        df["roe_score"] = normalize(
            df["return_on_equity_pct"]
        )

        df["roce_score"] = normalize(
            df["return_on_capital_employed_pct"]
        )

        df["npm_score"] = normalize(
            df["net_profit_margin_pct"]
        )

        # -------------------------
        # Efficiency Score
        # -------------------------

        df["asset_score"] = normalize(
            df["asset_turnover"]
        )

        # -------------------------
        # Debt Score (Lower is Better)
        # -------------------------

        debt_score = normalize(
            df["debt_to_equity"]
        )

        df["debt_score"] = 100 - debt_score

        # -------------------------
        # Final Weighted Quality Score
        # -------------------------

        df["quality_score"] = (
            df["roe_score"] * 0.25 +
            df["roce_score"] * 0.25 +
            df["npm_score"] * 0.15 +
            df["debt_score"] * 0.20 +
            df["asset_score"] * 0.15
        )

        # -------------------------
        # Clean Year Column
        # -------------------------

        df["year"] = pd.to_numeric(
            df["year"],
            errors="coerce"
        )

        df = df[
            df["year"].notna()
        ]

        # -------------------------
        # Keep Latest Year Per Company
        # -------------------------

        df = (
            df.sort_values("year")
              .groupby("company_id")
              .tail(1)
        )

        # -------------------------
        # Remove Invalid Scores
        # -------------------------

        df = df[
            df["quality_score"].notna()
        ]

        # -------------------------
        # Rank Companies
        # -------------------------

        df["quality_rank"] = (
            df["quality_score"]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        # -------------------------
        # Sort Rankings
        # -------------------------

        df = (
            df.sort_values("quality_rank")
              .reset_index(drop=True)
        )

        # -------------------------
        # Save to SQLite
        # -------------------------

        df.to_sql(
            "rankings",
            conn,
            if_exists="replace",
            index=False
        )

        print("Rankings created:", len(df))


if __name__ == "__main__":
    create_rankings()
    