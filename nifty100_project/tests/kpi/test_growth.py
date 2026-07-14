from analytics.growth import (
    revenue_growth,
    profit_growth
)


def test_revenue_growth():
    assert revenue_growth(120, 100) == 20


def test_revenue_decline():
    assert revenue_growth(80, 100) == -20


def test_revenue_zero_base():
    assert revenue_growth(100, 0) is None


def test_profit_growth():
    assert profit_growth(150, 100) == 50


def test_profit_decline():
    assert profit_growth(80, 100) == -20


def test_profit_zero_base():
    assert profit_growth(50, 0) is None