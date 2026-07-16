import pandas as pd
from pathlib import Path


OUTPUT_PATH = Path(__file__).resolve().parents[2] / "output"


def create_portfolio():

    print("Loading investment ranking...")

    df = pd.read_excel(
        OUTPUT_PATH / "investment_ranking.xlsx"
    )


    # Select BUY stocks
    portfolio = df[
        df["recommendation"] == "BUY"
    ].copy()


    # Top 10 companies
    portfolio = portfolio.head(10).copy()


    if portfolio.empty:
        print("No BUY stocks found.")
        return


    # Allocation

    allocation = round(
        100 / len(portfolio),
        2
    )

    portfolio["allocation_percentage"] = allocation


    # Risk classification

    def risk_level(score):

        if score >= 80:
            return "Low Risk"

        elif score >= 60:
            return "Medium Risk"

        else:
            return "High Risk"


    portfolio["risk_category"] = portfolio[
        "investment_score"
    ].apply(risk_level)


    final = portfolio[
        [
            "company_id",
            "company_name",
            "investment_score",
            "recommendation",
            "allocation_percentage",
            "risk_category"
        ]
    ]


    final.to_excel(
        OUTPUT_PATH / "final_portfolio.xlsx",
        index=False
    )


    print("Final portfolio created.")
    print(final)



if __name__ == "__main__":
    create_portfolio()