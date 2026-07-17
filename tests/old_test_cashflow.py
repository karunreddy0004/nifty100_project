import pytest

from analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


def test_free_cash_flow():
    assert free_cash_flow(100, -40) == 60


def test_free_cash_flow_negative():
    assert free_cash_flow(-20, -30) == -50


def test_cfo_quality_high():
    assert cfo_quality_score(120, 100) == "High Quality"


def test_cfo_quality_moderate():
    assert cfo_quality_score(70, 100) == "Moderate"


def test_cfo_quality_accrual():
    assert cfo_quality_score(30, 100) == "Accrual Risk"


def test_cfo_quality_pat_zero():
    assert cfo_quality_score(100, 0) is None


def test_capex_intensity():
    value, label = capex_intensity(-50, 1000)
    assert round(value, 2) == 5.00
    assert label == "Moderate"


def test_fcf_conversion():
    assert fcf_conversion_rate(60, 120) == 50


def test_fcf_conversion_zero():
    assert fcf_conversion_rate(50, 0) is None


def test_capital_allocation():
    assert capital_allocation_pattern(100, -50, -20) == "Reinvestor"