import pytest
from etl.normaliser import normalize_year, normalize_ticker


# -----------------------------
# normalize_year tests (20)
# -----------------------------

@pytest.mark.parametrize("input_value,expected", [
    ("FY22", 2022),
    ("FY23", 2023),
    ("FY24", 2024),
    ("2022", 2022),
    ("2021", 2021),
    ("2020-21", 2020),
    ("2019-20", 2019),
    ("Dec 2012", 2012),
    ("Mar 2018", 2018),
    ("Jun 2017", 2017),
    ("Sep 2016", 2016),
    ("2015 Annual", 2015),
    ("FY15", 2015),
    ("FY16", 2016),
    ("FY17", 2017),
    (" FY18 ", 2018),
    (2022, 2022),
    ("abcd", None),
    ("", None),
    (None, None),
])
def test_normalize_year(input_value, expected):
    assert normalize_year(input_value) == expected


# -----------------------------
# normalize_ticker tests (15)
# -----------------------------

@pytest.mark.parametrize("input_value,expected", [
    ("tcs", "TCS"),
    ("infy", "INFY"),
    ("reliance", "RELIANCE"),
    ("HDFCBANK", "HDFCBANK"),
    ("SBIN.NS", "SBIN"),
    ("INFY.NS", "INFY"),
    ("tcs.ns", "TCS"),
    (" abb ", "ABB"),
    (" adanient ", "ADANIENT"),
    ("LT", "LT"),
    ("lt.ns", "LT"),
    ("", ""),
    ("  ", ""),
    (None, None),
    ("ICICIBANK", "ICICIBANK"),
])
def test_normalize_ticker(input_value, expected):
    assert normalize_ticker(input_value) == expected