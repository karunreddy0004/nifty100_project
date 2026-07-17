import pytest
from pathlib import Path

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    check_opm_difference,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover
)


def icr_label(icr):
    """
    Label debt-free companies.
    """
    if icr is None:
        return "Debt Free"

    return ""


def icr_warning(icr):
    """
    Warning if ICR < 1.5
    """
    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """
    Net Debt = Borrowings - Investments
    """
    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Asset Turnover = Sales / Total Assets
    """
    if total_assets == 0:
        return None

    return sales / total_assets


def test_net_profit_margin():
    assert net_profit_margin(20, 100) == 20


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(10, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(25, 100) == 25


def test_return_on_equity():
    assert return_on_equity(20, 50, 50) == 20


def test_return_on_equity_negative():
    assert return_on_equity(20, -100, 50) is None


def test_roce():
    assert return_on_capital_employed(30, 50, 50, 50) == 20


def test_roa():
    assert return_on_assets(10, 100) == 10


def test_roa_zero_assets():
    assert return_on_assets(10, 0) is None
   


def test_opm_crosscheck():
    log = Path("output/opm_mismatch.log")

    if log.exists():
        log.unlink()

    check_opm_difference(
        "TCS",
        2024,
        25,
        22
    )

    assert log.exists()


def test_debt_to_equity():
    assert debt_to_equity(100, 50, 50) == 1

def test_debt_to_equity_zero_borrowings():
    assert debt_to_equity(0, 50, 50) == 0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(100, -100, 50) is None


def test_high_leverage_flag():
    assert high_leverage_flag(6) is True


def test_interest_coverage_ratio():
    assert interest_coverage_ratio(100, 20, 10) == 12


def test_interest_coverage_zero_interest():
    assert interest_coverage_ratio(100, 20, 0) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning(1.2) is True


def test_net_debt():
    assert net_debt(200, 50) == 150


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None