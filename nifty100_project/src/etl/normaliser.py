import re


def normalize_year(value):
    if value is None:
        return None

    value = str(value).strip()

    if re.fullmatch(r"\d{4}", value):
        return int(value)

    match = re.fullmatch(r"FY(\d{2})", value, re.IGNORECASE)
    if match:
        return 2000 + int(match.group(1))

    match = re.match(r"(\d{4})-\d{2}", value)
    if match:
        return int(match.group(1))

    match = re.search(r"(\d{4})", value)
    if match:
        return int(match.group(1))

    return None


def normalize_ticker(ticker):
    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    if ticker.endswith(".NS"):
        ticker = ticker[:-3]

    return ticker