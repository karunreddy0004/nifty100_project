from src.analytics.valuation import (
    earnings_yield,
    book_value_per_share,
    price_to_book,
    peg_ratio,
    market_cap_category
)


def test_earnings_yield():
    assert earnings_yield(20, 200) == 10


def test_earnings_yield_zero_price():
    assert earnings_yield(20, 0) is None


def test_book_value():
    assert book_value_per_share(100, 100, 20) == 10


def test_book_value_zero_shares():
    assert book_value_per_share(100, 100, 0) is None


def test_price_to_book():
    assert price_to_book(200, 100) == 2


def test_price_to_book_zero():
    assert price_to_book(200, 0) is None


def test_peg_ratio():
    assert peg_ratio(20, 10) == 2


def test_peg_ratio_zero_growth():
    assert peg_ratio(20, 0) is None


def test_market_cap_large():
    assert market_cap_category(300000) == "Large Cap"


def test_market_cap_mid():
    assert market_cap_category(100000) == "Mid Cap"


def test_market_cap_small():
    assert market_cap_category(10000) == "Small Cap"