def growth_rate(current, previous):
    """
    Growth % = ((Current - Previous) / Previous) * 100
    """
    if previous == 0:
        return None

    return ((current - previous) / previous) * 100


def revenue_growth(current_sales, previous_sales):
    return growth_rate(current_sales, previous_sales)


def profit_growth(current_profit, previous_profit):
    return growth_rate(current_profit, previous_profit)