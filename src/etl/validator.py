import pandas as pd
from pathlib import Path


class DataValidator:

    def __init__(self, datasets):
        self.datasets = datasets
        self.failures = []

    def add_failure(self, dq_rule, severity, table, row_id, message):
        self.failures.append({
            "dq_rule": dq_rule,
            "severity": severity,
            "table": table,
            "row_id": row_id,
            "message": message
        })

    # -----------------------
    # DQ-01: Company ID must be unique
    # -----------------------
    def dq01_company_pk_unique(self):
        df = self.datasets["companies"]

        duplicates = df[df["id"].duplicated(keep=False)]

        for _, row in duplicates.iterrows():
            self.add_failure(
                dq_rule="DQ-01",
                severity="CRITICAL",
                table="companies",
                row_id=row["id"],
                message="Duplicate company id"
            )

    # -----------------------
    # DQ-02: (company_id, year) must be unique
    # -----------------------
    def dq02_company_year_unique(self):

        tables = [
            "profitandloss",
            "balancesheet",
            "cashflow"
        ]

        for table in tables:

            df = self.datasets[table]

            duplicates = df[df.duplicated(
                subset=["company_id", "year"],
                keep=False
            )]

            for _, row in duplicates.iterrows():

                self.add_failure(
                    dq_rule="DQ-02",
                    severity="CRITICAL",
                    table=table,
                    row_id=row["id"],
                    message="Duplicate company_id + year"
                )

    # -----------------------
    # DQ-03: Foreign Key Integrity
    # -----------------------
    def dq03_foreign_key_integrity(self):

        companies = self.datasets["companies"]
        valid_ids = set(companies["id"])

        tables = [
            "profitandloss",
            "balancesheet",
            "cashflow"
        ]

        for table in tables:

            df = self.datasets[table]

            invalid_rows = df[~df["company_id"].isin(valid_ids)]

            for _, row in invalid_rows.iterrows():

                self.add_failure(
                    dq_rule="DQ-03",
                    severity="CRITICAL",
                    table=table,
                    row_id=row["id"],
                    message=f"Invalid company_id {row['company_id']}"
                )

        # -----------------------
    # DQ-04: Balance Sheet Check
    # -----------------------
    def dq04_balance_sheet_check(self):

        df = self.datasets["balancesheet"]

        for _, row in df.iterrows():

            liabilities = (
                row["equity_capital"] +
                row["reserves"] +
                row["borrowings"] +
                row["other_liabilities"]
            )

            assets = (
                row["fixed_assets"] +
                row["cwip"] +
                row["investments"] +
                row["other_asset"]
            )

            if row["total_liabilities"] != 0:
                liability_diff = abs(liabilities - row["total_liabilities"]) / row["total_liabilities"]
            else:
                liability_diff = 0

            if row["total_assets"] != 0:
                asset_diff = abs(assets - row["total_assets"]) / row["total_assets"]
            else:
                asset_diff = 0

            if liability_diff > 0.01:
                self.add_failure(
                    dq_rule="DQ-04",
                    severity="WARNING",
                    table="balancesheet",
                    row_id=row["id"],
                    message="Liabilities do not balance within 1%"
                )

            if asset_diff > 0.01:
                self.add_failure(
                    dq_rule="DQ-04",
                    severity="WARNING",
                    table="balancesheet",
                    row_id=row["id"],
                    message="Assets do not balance within 1%"
                )

        # -----------------------
    # DQ-05: OPM Cross Check
    # -----------------------
    def dq05_opm_cross_check(self):

        df = self.datasets["profitandloss"]

        for _, row in df.iterrows():

            if row["sales"] == 0:
                continue

            calculated_opm = (row["operating_profit"] / row["sales"]) * 100

            difference = abs(calculated_opm - row["opm_percentage"])

            if difference > 1:

                self.add_failure(
                    dq_rule="DQ-05",
                    severity="WARNING",
                    table="profitandloss",
                    row_id=row["id"],
                    message=f"OPM mismatch ({difference:.2f}%)"
                )

        # -----------------------
    # DQ-06: Positive Sales
    # -----------------------
    def dq06_positive_sales(self):

        df = self.datasets["profitandloss"]

        for _, row in df.iterrows():

            if row["sales"] < 0:

                self.add_failure(
                    dq_rule="DQ-06",
                    severity="CRITICAL",
                    table="profitandloss",
                    row_id=row["id"],
                    message="Negative sales value"
                )
        # -----------------------
    # DQ-07: Net Cash Flow Check
    # -----------------------
    def dq07_net_cash_flow(self):

        df = self.datasets["cashflow"]

        for _, row in df.iterrows():

            calculated = (
                row["operating_activity"] +
                row["investing_activity"] +
                row["financing_activity"]
            )

            difference = abs(calculated - row["net_cash_flow"])

            if difference > 1:

                self.add_failure(
                    dq_rule="DQ-07",
                    severity="WARNING",
                    table="cashflow",
                    row_id=row["id"],
                    message=f"Net cash flow mismatch ({difference})"
                )
    
        # -----------------------
    # DQ-08: Tax Percentage Check
    # -----------------------
    def dq08_tax_percentage(self):

        df = self.datasets["profitandloss"]

        for _, row in df.iterrows():

            tax = row["tax_percentage"]

            if tax < 0 or tax > 100:

                self.add_failure(
                    dq_rule="DQ-08",
                    severity="WARNING",
                    table="profitandloss",
                    row_id=row["id"],
                    message=f"Invalid tax percentage ({tax})"
                )
    
        # -----------------------
    # DQ-09: Dividend Payout Check
    # -----------------------
    def dq09_dividend_payout(self):

        df = self.datasets["profitandloss"]

        for _, row in df.iterrows():

            payout = row["dividend_payout"]

            if payout < 0 or payout > 100:

                self.add_failure(
                    dq_rule="DQ-09",
                    severity="WARNING",
                    table="profitandloss",
                    row_id=row["id"],
                    message=f"Invalid dividend payout ({payout})"
                )

        # -----------------------
    # DQ-10: Website URL Validation
    # -----------------------
    def dq10_website_url(self):

        df = self.datasets["companies"]

        for _, row in df.iterrows():

            website = str(row["website"]).strip()

            if not (
                website.startswith("http://")
                or website.startswith("https://")
            ):

                self.add_failure(
                    dq_rule="DQ-10",
                    severity="WARNING",
                    table="companies",
                    row_id=row["id"],
                    message="Invalid website URL"
                )
        # -----------------------
    # DQ-11: EPS Sign Check
    # -----------------------
    def dq11_eps_sign(self):

        df = self.datasets["profitandloss"]

        for _, row in df.iterrows():

            if row["net_profit"] > 0 and row["eps"] < 0:

                self.add_failure(
                    dq_rule="DQ-11",
                    severity="WARNING",
                    table="profitandloss",
                    row_id=row["id"],
                    message="Positive profit but negative EPS"
                )
        # -----------------------
    # DQ-12: Annual Report URL Check
    # -----------------------
    def dq12_document_url(self):

        df = self.datasets["documents"]

        for _, row in df.iterrows():

            url = str(row["Annual_Report"]).strip()

            if not (
                url.startswith("http://")
                or url.startswith("https://")
            ):

                self.add_failure(
                    dq_rule="DQ-12",
                    severity="WARNING",
                    table="documents",
                    row_id=row["id"],
                    message="Invalid Annual Report URL"
                )
        # -----------------------
    # DQ-13: Stock Price Validation
    # -----------------------
    def dq13_stock_price(self):

        df = self.datasets["stock_prices"]

        for _, row in df.iterrows():

            if (
                row["high_price"] < row["open_price"]
                or row["high_price"] < row["close_price"]
                or row["low_price"] > row["open_price"]
                or row["low_price"] > row["close_price"]
            ):

                self.add_failure(
                    dq_rule="DQ-13",
                    severity="WARNING",
                    table="stock_prices",
                    row_id=row["id"],
                    message="Invalid OHLC prices"
                )
        # -----------------------
    # DQ-14: Market Cap Positive
    # -----------------------
    def dq14_market_cap(self):

        df = self.datasets["market_cap"]

        for _, row in df.iterrows():

            if row["market_cap_crore"] <= 0:

                self.add_failure(
                    dq_rule="DQ-14",
                    severity="WARNING",
                    table="market_cap",
                    row_id=row["id"],
                    message="Market cap must be positive"
                )
        # -----------------------
    # DQ-15: Sector Weight Check
    # -----------------------
    def dq15_sector_weight(self):

        df = self.datasets["sectors"]

        for _, row in df.iterrows():

            weight = row["index_weight_pct"]

            if weight < 0 or weight > 100:

                self.add_failure(
                    dq_rule="DQ-15",
                    severity="WARNING",
                    table="sectors",
                    row_id=row["id"],
                    message="Invalid sector weight"
                )
        # -----------------------
    # DQ-16: Peer Group Benchmark Check
    # -----------------------
    def dq16_peer_group(self):

        df = self.datasets["peer_groups"]

        for _, row in df.iterrows():

            value = str(row["is_benchmark"]).strip().lower()

            if value not in ["true", "false"]:

                self.add_failure(
                    dq_rule="DQ-16",
                    severity="WARNING",
                    table="peer_groups",
                    row_id=row["id"],
                    message="Invalid benchmark value"
                )
    

    def save_report(self, output_path="output/validation_failures.csv"):

        Path("output").mkdir(exist_ok=True)

        df = pd.DataFrame(self.failures)

        if df.empty:
            df = pd.DataFrame(columns=[
                "dq_rule",
                "severity",
                "table",
                "row_id",
                "message"
            ])

        df.to_csv(output_path, index=False)

        print(f"Validation report saved to {output_path}")

    # ✅ run_all is now a proper class method, NOT inside save_report
    def run_all(self):
        print("Running Data Quality Checks...")

        self.dq01_company_pk_unique()
        self.dq02_company_year_unique()
        self.dq03_foreign_key_integrity()
        self.dq04_balance_sheet_check() 
        self.dq05_opm_cross_check()
        self.dq06_positive_sales()
        self.dq07_net_cash_flow()
        self.dq08_tax_percentage()
        self.dq09_dividend_payout()
        self.dq10_website_url()
        self.dq11_eps_sign()
        self.dq12_document_url()
        self.dq13_stock_price()
        self.dq14_market_cap()
        self.dq15_sector_weight()
        self.dq16_peer_group()
        self.save_report()


if __name__ == "__main__":

    data_path = Path("data/raw")

    datasets = {
        "companies": pd.read_excel(data_path / "companies.xlsx", header=1),
        "profitandloss": pd.read_excel(data_path / "profitandloss.xlsx", header=1),
        "balancesheet": pd.read_excel(data_path / "balancesheet.xlsx", header=1),
        "cashflow": pd.read_excel(data_path / "cashflow.xlsx", header=1),
        "financial_ratios": pd.read_excel(data_path / "financial_ratios.xlsx",header=1),
        "documents": pd.read_excel(data_path / "documents.xlsx", header=1),
        "market_cap": pd.read_excel(data_path / "market_cap.xlsx",header=1),
        "peer_groups": pd.read_excel(data_path / "peer_groups.xlsx",header=1),
        "sectors": pd.read_excel(data_path / "sectors.xlsx",header=1),
        "stock_prices": pd.read_excel(data_path / "stock_prices.xlsx",header=1),
    }

    validator = DataValidator(datasets)
    validator.run_all()