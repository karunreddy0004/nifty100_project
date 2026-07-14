import pandas as pd

from analytics.ranking import (
    score_roe,
    score_roce,
    score_margin,
    total_score,
    rank_companies
)


def test_score_roe():
    assert score_roe(25) == 5


def test_score_roce():
    assert score_roce(16) == 4


def test_score_margin():
    assert score_margin(12) == 3


def test_total_score():
    row = {
        "return_on_equity_pct": 25,
        "return_on_capital_employed_pct": 16,
        "net_profit_margin_pct": 12,
    }
    assert total_score(row) == 12


def test_rank_companies():
    df = pd.DataFrame([
        {
            "company_id": "A",
            "return_on_equity_pct": 25,
            "return_on_capital_employed_pct": 20,
            "net_profit_margin_pct": 15,
        },
        {
            "company_id": "B",
            "return_on_equity_pct": 10,
            "return_on_capital_employed_pct": 10,
            "net_profit_margin_pct": 10,
        },
    ])

    ranked = rank_companies(df)

    assert ranked.iloc[0]["company_id"] == "A"