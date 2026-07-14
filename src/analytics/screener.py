import sqlite3
import pandas as pd
import yaml

DB = "db/nifty100.db"
CONFIG = "config/screener_config.yaml"


def load_data():
    """Load rankings table from SQLite."""
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM rankings", conn)
    conn.close()
    return df


def load_config():
    """Load filter thresholds from YAML."""
    with open(CONFIG, "r") as f:
        return yaml.safe_load(f)


def apply_filters(df, filters):
    """Apply threshold filters."""
    result = df.copy()

    if "quality_score_min" in filters:
        result = result[
            result["quality_score"] >= filters["quality_score_min"]
        ]

    return result


def screen_stocks():
    df = load_data()
    config = load_config()

    filters = config.get("filters", {})

    filtered = apply_filters(df, filters)

    filtered = filtered.sort_values(
        by="quality_score",
        ascending=False
    )

    return filtered


def export_results(df):
    output_file = "output/screener.csv"
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":

    filtered = screen_stocks()

    print(filtered.head(20))

    print("Stocks found:", len(filtered))

    export_results(filtered)