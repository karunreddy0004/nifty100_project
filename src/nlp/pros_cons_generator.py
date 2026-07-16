import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


def load_latest_ratios():
    conn = sqlite3.connect(DB_FILE)

    query = """
    SELECT *
    FROM financial_ratios
    """

    df = pd.read_sql(query, conn)

    conn.close()

    latest = (
        df
        .sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .last()
    )

    return latest


def load_all_ratios():
    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios ORDER BY company_id, year",
        conn
    )

    conn.close()

    return df
def apply_pro_rules(latest, all_ratios):

    results = []

    for _, row in latest.iterrows():

        # -------------------------------------------------
        # PRO RULE P01
        # ROE > 20%
        # -------------------------------------------------
        if (
            pd.notna(row["return_on_equity_pct"])
            and row["return_on_equity_pct"] > 0.20
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Pro",
                "rule_id": "P01",
                "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",
                "confidence_pct": 90
            })

        # -------------------------------------------------
        # PRO RULE P03
        # Debt Free Company
        # ------------------------------------------------
        if (
            pd.notna(row["debt_to_equity"])
            and row["debt_to_equity"] == 0
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Pro",
                "rule_id": "P03",
                "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden",
                "confidence_pct": 95
            })

        # -------------------------------------------------
        # Last 5 years history
        # -------------------------------------------------
        history = (
            all_ratios[
                (all_ratios["company_id"] == row["company_id"])
                & (all_ratios["year"].notna())
            ]
            .sort_values("year")
            .tail(5)
        )

        # -------------------------------------------------
        # PRO RULE P02
        # Positive Free Cash Flow for 5 consecutive years
        # -------------------------------------------------
        if (
            len(history) == 5
            and history["free_cash_flow"].notna().all()
            and (history["free_cash_flow"] > 0).all()
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Pro",
                "rule_id": "P02",
                "text": "Strong free cash flow generation over 5 years signals healthy business fundamentals",
                "confidence_pct": 92
            })
        # -------------------------------------------------
        # CON RULE C02
        # Negative Free Cash Flow for last 3 years
        # -------------------------------------------------

        last3 = history.tail(3)

        if (
            len(last3) == 3
            and last3["free_cash_flow"].notna().all()
            and (last3["free_cash_flow"] < 0).all()
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Con",
                "rule_id": "C02",
                "text": "Negative free cash flow for three consecutive years may indicate weak cash generation.",
                "confidence_pct": 92
            })
        # -------------------------------------------------
        # CON RULE C03
        # Debt to Equity > 1.5
        # -------------------------------------------------

        if (
            pd.notna(row["debt_to_equity"])
            and row["debt_to_equity"] > 1.5
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Con",
                "rule_id": "C03",
                "text": "High debt levels increase financial risk and interest burden.",
                "confidence_pct": 91
            })



         # -------------------------------------------------
        # PRO RULE P04
        # Revenue CAGR > 15%
        # -------------------------------------------------
        if (
            pd.notna(row["revenue_cagr_5yr"])
            and row["revenue_cagr_5yr"] > 15
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Pro",
                "rule_id": "P04",
                "text": "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum",
                "confidence_pct": 88
            })
        # -------------------------------------------------
        # CON RULE C05
        # Revenue CAGR below 5%
        # -------------------------------------------------
        if (
            pd.notna(row["revenue_cagr_5yr"])
            and row["revenue_cagr_5yr"] < 5
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Con",
                "rule_id": "C05",
                "text": "Revenue growth below 5% over five years indicates slow business expansion.",
                "confidence_pct": 88
            })
        # -------------------------------------------------
        # PRO RULE P05
        # Operating Profit Margin > 25%
        # -------------------------------------------------
        if (
            pd.notna(row["operating_profit_margin_pct"])
            and row["operating_profit_margin_pct"] > 25
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Pro",
                "rule_id": "P05",
                "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline",
                "confidence_pct": 89
            })
        # -------------------------------------------------
        # CON RULE C06
        # Negative Free Cash Flow in latest year
        # -------------------------------------------------
        if (
            pd.notna(row["free_cash_flow"])
            and row["free_cash_flow"] < 0
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Con",
                "rule_id": "C06",
                "text": "Negative free cash flow may indicate pressure on cash generation and future investments",
                "confidence_pct": 90
            })
                # -------------------------------------------------
        # PRO RULE P06
        # PAT CAGR > 20%
        # -------------------------------------------------
        if (
            pd.notna(row["pat_cagr_5yr"])
            and row["pat_cagr_5yr"] > 20
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Pro",
                "rule_id": "P06",
                "text": "Net profit compounding at above 20% over 5 years creates significant shareholder value",
                "confidence_pct": 90
            })
                # -------------------------------------------------
        # PRO RULE P07
        # Interest Coverage > 10 OR Debt Free
        # -------------------------------------------------
        if (
            (pd.notna(row["interest_coverage"]) and row["interest_coverage"] > 10)
            or
            (pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] == 0)
        ):
            results.append({
                "company_id": row["company_id"],
                "type": "Pro",
                "rule_id": "P07",
                "text": "Very high interest coverage ratio reflects negligible financial stress from debt servicing",
                "confidence_pct": 91
            })
            # -------------------------------------------------
            # PRO RULE P08
            # Asset Turnover > 1.5
            # -------------------------------------------------
            if (
                pd.notna(row["asset_turnover"])
                and row["asset_turnover"] > 1.0
            ):
                results.append({
                    "company_id": row["company_id"],
                    "type": "Pro",
                    "rule_id": "P08",
                    "text": "Efficient utilization of assets reflects strong operating efficiency",
                    "confidence_pct": 87
                })
            # -------------------------------------------------
            # PRO RULE P09
            # ROCE > 20%
            # -------------------------------------------------
            if (
                pd.notna(row["return_on_capital_employed_pct"])
                and row["return_on_capital_employed_pct"] > 20
            ):
                results.append({
                    "company_id": row["company_id"],
                    "type": "Pro",
                    "rule_id": "P09",
                    "text": "High return on capital employed indicates efficient utilization of long-term capital",
                    "confidence_pct": 90
                })
            # -------------------------------------------------
            # PRO RULE P10
            # CFO/PAT Ratio > 1
            # -------------------------------------------------
            if (
                pd.notna(row["cfo_pat_ratio"])
                and row["cfo_pat_ratio"] > 1
            ):
                results.append({
                    "company_id": row["company_id"],
                    "type": "Pro",
                    "rule_id": "P10",
                    "text": "Strong cash conversion with operating cash flow consistently supporting reported profits",
                    "confidence_pct": 90
                })

            # -------------------------------------------------
            # CON RULE C01
            # ROE < 10%
            # -------------------------------------------------
            if (
                pd.notna(row["return_on_equity_pct"])
                and row["return_on_equity_pct"] < 0.10
            ):
                results.append({
                    "company_id": row["company_id"],
                    "type": "Con",
                    "rule_id": "C01",
                    "text": "Low return on equity indicates weak shareholder returns",
                    "confidence_pct": 90
                })
                    

    return pd.DataFrame(results)
if __name__ == "__main__":

    latest = load_latest_ratios()
    all_ratios = load_all_ratios()

    print("Latest Companies :", len(latest))
    print("Historical Rows :", len(all_ratios))

    pros_cons_df = apply_pro_rules(latest, all_ratios)

    print()
    print(pros_cons_df.head(20))

    print()
    print("Generated Records:", len(pros_cons_df))

    conn = sqlite3.connect(DB_FILE)

    pros_cons_df.to_sql(
        "pros_cons",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print()
    print("Saved to SQLite table: pros_cons")

    output_file = OUTPUT_DIR / "pros_cons_generated.csv"
    pros_cons_df.to_csv(output_file, index=False)

    print("CSV Saved:")
    print(output_file)