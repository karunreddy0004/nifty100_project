PRESETS = {

    "quality_compounder": {
        "return_on_equity_pct": {"min": 15},
        "debt_to_equity": {"max": 1.0},
        "free_cash_flow": {"min": 0},
        "revenue_cagr_5yr": {"min": 10}
    },

    "value_pick": {
        "pe_ratio": {"max": 20},
        "pb_ratio": {"max": 3},
        "debt_to_equity": {"max": 2},
        "dividend_yield_pct": {"min": 1}
    },

    "growth_accelerator": {
        "pat_cagr_5yr": {"min": 20},
        "revenue_cagr_5yr": {"min": 15},
        "debt_to_equity": {"max": 2}
    },

    "dividend_champion": {
        "dividend_yield_pct": {"min": 2},
        "dividend_payout": {"max": 80},
        "free_cash_flow": {"min": 0}
    },

    "debt_free_bluechip": {
        "debt_to_equity": {"max": 0},
        "return_on_equity_pct": {"min": 12},
        "sales": {"min": 5000}
    },

    "turnaround_watch": {
        "revenue_cagr_3yr": {"min": 10},
        "free_cash_flow": {"min": 0}
    }

}


from engine import load_data
from engine import apply_filters


def run_preset(name):

    df = load_data()

    if name not in PRESETS:
        raise ValueError(f"Unknown preset: {name}")

    config = PRESETS[name]

    result = apply_filters(df, config)

    return result