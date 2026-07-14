def earnings_yield(eps, market_price):
    """
    Earnings Yield = EPS / Market Price × 100
    """
    if market_price == 0:
        return None

    return (eps / market_price) * 100


def book_value_per_share(equity, reserves, shares):
    """
    Book Value Per Share
    """
    if shares == 0:
        return None

    return (equity + reserves) / shares


def price_to_book(market_price, book_value):
    """
    Price to Book Ratio
    """
    if book_value in (0, None):
        return None

    return market_price / book_value


def peg_ratio(pe, growth):
    """
    PEG Ratio
    """
    if growth in (0, None):
        return None

    return pe / growth


def market_cap_category(market_cap):
    """
    Company size category
    """
    if market_cap >= 200000:
        return "Large Cap"

    if market_cap >= 50000:
        return "Mid Cap"

    return "Small Cap"