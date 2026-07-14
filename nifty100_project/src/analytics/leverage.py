def debt_to_equity(borrowings, equity, reserves):
    capital = equity + reserves

    if borrowings == 0:
        return 0

    if capital <= 0:
        return None

    return borrowings / capital


def high_leverage_flag(debt_equity):
    if debt_equity is None:
        return False
    return debt_equity > 5


def interest_coverage_ratio(operating_profit, other_income, interest):
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(icr):
    if icr is None:
        return "Debt Free"
    return ""


def icr_warning(icr):
    if icr is None:
        return False
    return icr < 1.5


def net_debt(borrowings, investments):
    return borrowings - investments


def asset_turnover(sales, total_assets):
    if total_assets == 0:
        return None
    return sales / total_assets
