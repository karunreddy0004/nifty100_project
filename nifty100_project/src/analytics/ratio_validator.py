import sqlite3
import pandas as pd


DB = "db/nifty100.db"


def validate_ratios():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )


    print("Before cleaning:")
    print(df.shape)


    # remove invalid years

    df = df[
        df["year"].notna()
    ]


    # remove duplicate company-year

    df = df.drop_duplicates(
        subset=[
            "company_id",
            "year"
        ]
    )


    # cap extreme ratios for scoring

    ratio_columns = [
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "return_on_assets_pct",
        "return_on_capital_employed_pct"
    ]


    for col in ratio_columns:

        df[col] = df[col].clip(
            lower=-100,
            upper=500
        )


    df.to_sql(
        "financial_ratios",
        conn,
        if_exists="replace",
        index=False
    )


    conn.close()


    print("After cleaning:")
    print(df.shape)

    print("Ratio validation completed")


if __name__ == "__main__":
    validate_ratios()