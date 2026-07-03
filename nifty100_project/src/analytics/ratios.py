def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = Net Profit / Sales * 100
    """
    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin
    """
    if sales == 0:
        return None

    return (operating_profit / sales) * 100


def return_on_equity(net_profit, equity, reserves):
    """
    ROE = Net Profit / (Equity + Reserves)
    """
    capital = equity + reserves

    if capital <= 0:
        return None

    return (net_profit / capital) * 100


def return_on_capital_employed(ebit, equity, reserves, borrowings):
    """
    ROCE = EBIT / (Equity + Reserves + Borrowings)
    """
    capital = equity + reserves + borrowings

    if capital <= 0:
        return None

    return (ebit / capital) * 100


def return_on_assets(net_profit, total_assets):
    """
    ROA = Net Profit / Total Assets
    """
    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100

from pathlib import Path

LOG_FILE = Path("output/opm_mismatch.log")

def check_opm_difference(company_id, year, calculated_opm, source_opm):
    if calculated_opm is None or source_opm is None:
        return

    difference = abs(calculated_opm - source_opm)

    if difference > 1:
        with open(LOG_FILE, "a") as f:
            f.write(
                f"{company_id},{year},Calculated={calculated_opm:.2f},"
                f"Source={source_opm:.2f},Diff={difference:.2f}\n"
            )
def debt_to_equity(borrowings, equity, reserves):
    """
    Debt to Equity = Borrowings / (Equity + Reserves)
    """
    capital = equity + reserves

    if borrowings == 0:
        return 0

    if capital <= 0:
        return None

    return borrowings / capital


def high_leverage_flag(debt_equity):
    """
    High leverage if D/E > 5
    """
    if debt_equity is None:
        return False

    return debt_equity > 5


def interest_coverage_ratio(operating_profit, other_income, interest):
    """
    Interest Coverage Ratio = (Operating Profit + Other Income) / Interest
    """
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


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