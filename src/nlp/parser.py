import re
import sqlite3
import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# Project Paths
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = BASE_DIR / "data" / "raw" / "analysis.xlsx"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------
# Load Analysis Data
# ---------------------------------------------------

def load_analysis_data():
    """Load analysis.xlsx"""

    df = pd.read_excel(DATA_FILE, header=1)

    print(f"Loaded {len(df)} records")

    return df


# ---------------------------------------------------
# Parse Growth Text
# ---------------------------------------------------

def parse_growth_text(text):
    """
    Parse text like:
    10 Years: 21%

    Returns:
    (period_years, value_pct)
    """

    pattern = r"(\d+)\s*Years?:?\s*([\d.]+)%"

    match = re.search(pattern, str(text))

    if match:
        period = int(match.group(1))
        value = float(match.group(2))
        return period, value

    return None


# ---------------------------------------------------
# Parse Entire Dataset
# ---------------------------------------------------

def parse_analysis_data(df):

    target_columns = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]

    parsed_records = []
    failed_records = []

    for _, row in df.iterrows():

        company = row["company_id"]

        for metric in target_columns:

            text = row[metric]

            result = parse_growth_text(text)

            if result:

                period, value = result

                parsed_records.append({
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": period,
                    "value_pct": value
                })

            else:

                failed_records.append({
                    "company_id": company,
                    "metric_type": metric,
                    "original_text": text
                })

    parsed_df = pd.DataFrame(parsed_records)
    failed_df = pd.DataFrame(failed_records)

    return parsed_df, failed_df


def load_financial_ratios():

    conn = sqlite3.connect(BASE_DIR / "db" / "nifty100.db")

    query = """
    SELECT
        company_id,
        year,
        revenue_cagr_5yr,
        pat_cagr_5yr
    FROM financial_ratios
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

def get_latest_ratios(ratios_df):
    """
    Keep only the latest financial ratio record for each company.
    """

    latest_df = (
        ratios_df
        .sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .last()
    )

    return latest_df

def validate_cagr(parsed_df, latest_ratios):
    """
    Compare parsed 5-year CAGR values with the calculated values
    from the financial_ratios table.
    """

    validation_results = []

    parsed_5yr = parsed_df[parsed_df["period_years"] == 5]

    for _, row in parsed_5yr.iterrows():

        company = row["company_id"]
        metric = row["metric_type"]
        parsed_value = row["value_pct"]

        ratio = latest_ratios[
            latest_ratios["company_id"] == company
        ]

        if ratio.empty:
            continue

        if metric == "compounded_sales_growth":
            calculated = ratio.iloc[0]["revenue_cagr_5yr"]

        elif metric == "compounded_profit_growth":
            calculated = ratio.iloc[0]["pat_cagr_5yr"]

        else:
            continue

        if pd.isna(calculated):
            continue

        difference = abs(parsed_value - calculated)

        validation_results.append({
            "company_id": company,
            "metric_type": metric,
            "parsed_value": parsed_value,
            "calculated_value": round(calculated, 2),
            "difference_pct": round(difference, 2),
            "review_required": difference > 5
        })

    return pd.DataFrame(validation_results)

# ---------------------------------------------------
# Main
# ---------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 29 - NLP ANALYSIS PARSER")
    print("=" * 60)

    df = load_analysis_data()
    ratios_df = load_financial_ratios()
    latest_ratios = get_latest_ratios(ratios_df)

    print("\nLatest Ratios")
    print(latest_ratios.head())

    print("\nCompanies:", len(latest_ratios))

    parsed_df, failed_df = parse_analysis_data(df)
    validation_df = validate_cagr(parsed_df, latest_ratios)

    parsed_file = OUTPUT_DIR / "analysis_parsed.csv"
    failed_file = OUTPUT_DIR / "parse_failures.csv"
    validation_file = OUTPUT_DIR / "cagr_validation.csv"

    parsed_df.to_csv(parsed_file, index=False)
    failed_df.to_csv(failed_file, index=False)
    validation_df.to_csv(validation_file, index=False)

    print(f"\nParsed Records : {len(parsed_df)}")
    print(f"Failed Records : {len(failed_df)}")

    print("\nSample Parsed Records")
    print(parsed_df.head())

    print("\nFiles Created")
    print(parsed_file)
    print(failed_file)

    print("\nDay 29 Parser - Version 1 Completed")
    print("\nValidation Results")
    print(validation_df.head())

    print(f"\nValidation Records : {len(validation_df)}")
    print(f"Review Required : {validation_df['review_required'].sum()}")

    print("\nValidation File")
    print(validation_file)

    print("\nDay 29 Parser Completed Successfully")