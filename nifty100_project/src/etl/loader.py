import pandas as pd
import sqlite3
from pathlib import Path
from normaliser import normalize_year, normalize_ticker

DATA_PATH = Path("data/raw")
DB_PATH = Path("db/nifty100.db")
AUDIT_PATH = Path("output/load_audit.csv")


class Loader:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.audit = []

    def log(self, table, status, rows):
        self.audit.append({
            "table": table,
            "status": status,
            "rows_loaded": rows
        })

    def load_df(self, df, table):
        df.to_sql(table, self.conn, if_exists="replace", index=False)

    # ---------------------------
    # READ EXCEL SAFELY
    # ---------------------------
    def read_excel(self, file):

        header_map = {
            "companies.xlsx": 1,
            "profitandloss.xlsx": 1,
            "balancesheet.xlsx": 1,
            "cashflow.xlsx": 1,
            "analysis.xlsx": 1,
            "documents.xlsx": 1,
            "financial_ratios.xlsx": 0,
            "market_cap.xlsx": 0,
            "peer_groups.xlsx": 0,
            "sectors.xlsx": 0,
            "stock_prices.xlsx": 0,
        }

        header = header_map.get(file, 0)

        df = pd.read_excel(DATA_PATH / file, header=header)
        df.columns = [str(c).strip().lower() for c in df.columns]

        return df

    # ---------------------------
    # COMPANIES
    # ---------------------------
    def load_companies(self):
        df = self.read_excel("companies.xlsx")
        df["id"] = df["id"].astype(str).str.upper().str.strip()

        self.load_df(df, "companies")
        self.log("companies", "SUCCESS", len(df))

    # ---------------------------
    # PROFIT & LOSS
    # ---------------------------
    def load_profit_and_loss(self):
        df = self.read_excel("profitandloss.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)
        df["year"] = df["year"].apply(normalize_year)

        self.load_df(df, "profitandloss")
        self.log("profitandloss", "SUCCESS", len(df))

    # ---------------------------
    # BALANCE SHEET
    # ---------------------------
    def load_balance_sheet(self):
        df = self.read_excel("balancesheet.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)
        df["year"] = df["year"].apply(normalize_year)
        self.load_df(df, "balancesheet")
        self.log("balancesheet", "SUCCESS", len(df))

    # ---------------------------
    # CASHFLOW
    # ---------------------------
    def load_cashflow(self):
        df = self.read_excel("cashflow.xlsx")

        df["company_id"] = df["company_id"].apply(normalize_ticker)
        df["year"] = df["year"].apply(normalize_year)

        df = df[df["year"].notna()]
        df = df.drop_duplicates(subset=["company_id", "year"], keep="last")

        self.load_df(df, "cashflow")
        self.log("cashflow", "SUCCESS", len(df))


    # ---------------------------
    # ANALYSIS
    # ---------------------------
    def load_analysis(self):
        df = self.read_excel("analysis.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)

        self.load_df(df, "analysis")
        self.log("analysis", "SUCCESS", len(df))

    # ---------------------------
    # FINANCIAL RATIOS
    # ---------------------------
    def load_financial_ratios(self):
        df = self.read_excel("financial_ratios.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)
        df["year"] = df["year"].apply(normalize_year)

        self.load_df(df, "financial_ratios")
        self.log("financial_ratios", "SUCCESS", len(df))

    # ---------------------------
    # MARKET CAP
    # ---------------------------
    def load_market_cap(self):
        df = self.read_excel("market_cap.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)

        self.load_df(df, "market_cap")
        self.log("market_cap", "SUCCESS", len(df))

    # ---------------------------
    # SECTORS
    # ---------------------------
    def load_sectors(self):
        df = self.read_excel("sectors.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)

        self.load_df(df, "sectors")
        self.log("sectors", "SUCCESS", len(df))

    # ---------------------------
    # PEER GROUPS
    # ---------------------------
    def load_peer_groups(self):
        df = self.read_excel("peer_groups.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)

        self.load_df(df, "peer_groups")
        self.log("peer_groups", "SUCCESS", len(df))

    # ---------------------------
    # STOCK PRICES
    # ---------------------------
    def load_stock_prices(self):
        df = self.read_excel("stock_prices.xlsx")
        df["company_id"] = df["company_id"].apply(normalize_ticker)

        self.load_df(df, "stock_prices")
        self.log("stock_prices", "SUCCESS", len(df))

    # ---------------------------
    # RUN ALL
    # ---------------------------
    def run(self):

        print("Starting full ETL load...")

        self.load_companies()
        self.load_profit_and_loss()
        self.load_balance_sheet()
        self.load_cashflow()
        self.load_analysis()
        self.load_financial_ratios()
        self.load_market_cap()
        self.load_sectors()
        self.load_peer_groups()
        self.load_stock_prices()

        self.conn.commit()
        self.conn.close()

        pd.DataFrame(self.audit).to_csv(AUDIT_PATH, index=False)

        print("ETL complete ✔ Audit saved")


def load_all_files():
    loader = Loader()
    loader.run()


if __name__ == "__main__":
    load_all_files()