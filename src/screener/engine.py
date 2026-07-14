import sqlite3
import pandas as pd

DB = "db/nifty100.db"


# -----------------------------
# LOAD DATA
# -----------------------------

def load_data():

    conn = sqlite3.connect(DB)

    query = """

    SELECT

        fr.company_id,
        fr.year,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,

        fr.debt_to_equity,
        fr.interest_coverage,
        fr.asset_turnover,

        fr.free_cash_flow,
        fr.cfo_pat_ratio,

        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr,


        pl.sales,
        pl.net_profit,
        pl.eps,
        pl.dividend_payout,


        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.dividend_yield_pct,


        s.broad_sector,

        pg.peer_group_name


    FROM financial_ratios fr


    LEFT JOIN profitandloss pl
    ON fr.company_id = pl.company_id
    AND fr.year = pl.year


    LEFT JOIN market_cap mc
    ON fr.company_id = mc.company_id
    AND fr.year = mc.year


    LEFT JOIN sectors s
    ON fr.company_id = s.company_id


    LEFT JOIN peer_groups pg
    ON fr.company_id = pg.company_id

    """


    df = pd.read_sql(query, conn)

    conn.close()

    return df



# -----------------------------
# NORMALIZATION
# -----------------------------

def normalize_metric(series):

    p10 = series.quantile(0.10)
    p90 = series.quantile(0.90)

    clipped = series.clip(p10, p90)

    if p90 == p10:
        return pd.Series(
            50,
            index=series.index
        )

    return (
        (clipped - p10)
        /
        (p90 - p10)
    ) * 100



# -----------------------------
# COMPOSITE SCORE
# -----------------------------

def calculate_composite_score(df):


    profitability = (

        normalize_metric(
            df["return_on_equity_pct"].fillna(0)
        ) * 0.15

        +

        normalize_metric(
            df["return_on_capital_employed_pct"].fillna(0)
        ) * 0.10

        +

        normalize_metric(
            df["net_profit_margin_pct"].fillna(0)
        ) * 0.10

    )


    cash_quality = (

        normalize_metric(
            df["free_cash_flow"].fillna(0)
        ) * 0.15

        +

        normalize_metric(
            df["cfo_pat_ratio"].fillna(0)
        ) * 0.10

        +

        (df["free_cash_flow"] > 0)
        .astype(int)
        * 100
        * 0.05

    )


    growth = (

        normalize_metric(
            df["revenue_cagr_5yr"].fillna(0)
        ) * 0.10

        +

        normalize_metric(
            df["pat_cagr_5yr"].fillna(0)
        ) * 0.10

    )


    leverage = (

        normalize_metric(
            -df["debt_to_equity"].fillna(0)
        ) * 0.10

        +

        normalize_metric(
            df["interest_coverage"]
            .replace("Debt Free",100)
            .fillna(0)
        ) * 0.05

    )


    df["composite_quality_score"] = (

        profitability

        +

        cash_quality

        +

        growth

        +

        leverage

    )


    return df



# -----------------------------
# FILTER ENGINE
# -----------------------------

def apply_filters(df, filters):


    result = df.copy()



    if "roe_min" in filters:

        result = result[
            result["return_on_equity_pct"]
            >= filters["roe_min"]
        ]



    if "de_max" in filters:

        result = result[
            (result["broad_sector"]=="Financials")
            |
            (result["debt_to_equity"]
             <= filters["de_max"])
        ]



    if "fcf_min" in filters:

        result = result[
            result["free_cash_flow"]
            >= filters["fcf_min"]
        ]



    if "revenue_cagr_min" in filters:

        result = result[
            result["revenue_cagr_5yr"]
            >= filters["revenue_cagr_min"]
        ]



    if "pat_cagr_min" in filters:

        result = result[
            result["pat_cagr_5yr"]
            >= filters["pat_cagr_min"]
        ]



    if "pe_max" in filters:

        result = result[
            result["pe_ratio"]
            .fillna(999999)
            <= filters["pe_max"]
        ]



    if "pb_max" in filters:

        result = result[
            result["pb_ratio"]
            .fillna(999999)
            <= filters["pb_max"]
        ]



    if "dividend_yield_min" in filters:

        result = result[
            result["dividend_yield_pct"]
            .fillna(0)
            >= filters["dividend_yield_min"]
        ]



    if "sales_min" in filters:

        result = result[
            result["sales"]
            .fillna(0)
            >= filters["sales_min"]
        ]



    if len(result)>0:

        result = calculate_composite_score(result)

        result = result.sort_values(
            "composite_quality_score",
            ascending=False
        )


    return result




# -----------------------------
# PRESET SCREENERS
# -----------------------------


def quality_compounder(df):

    return apply_filters(
        df,
        {
            "roe_min":15,
            "de_max":1,
            "fcf_min":0,
            "revenue_cagr_min":10
        }
    )



def value_pick(df):

    return apply_filters(
        df,
        {
            "pe_max":20,
            "pb_max":3,
            "de_max":2,
            "dividend_yield_min":1
        }
    )



def growth_accelerator(df):

    return apply_filters(
        df,
        {
            "pat_cagr_min":20,
            "revenue_cagr_min":15,
            "de_max":2
        }
    )



def dividend_champion(df):

    result = apply_filters(
        df,
        {
            "dividend_yield_min":2
        }
    )

    result=result[
        result["dividend_payout"]<80
    ]

    result=result[
        result["free_cash_flow"]>0
    ]

    return result



def debt_free_bluechip(df):

    result=apply_filters(
        df,
        {
            "roe_min":12,
            "sales_min":5000
        }
    )

    return result[
        result["debt_to_equity"]==0
    ]



def turnaround_watch(df):

    result=df.copy()

    result=result[
        result["free_cash_flow"]>0
    ]

    result=result[
        result["revenue_cagr_5yr"]>10
    ]

    result=calculate_composite_score(result)

    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )



# -----------------------------
# MAIN
# -----------------------------

def main():


    print("Loading data...")

    df=load_data()

    print("Rows loaded:",len(df))


    presets={

        "Quality Compounder":
        quality_compounder(df),

        "Value Pick":
        value_pick(df),

        "Growth Accelerator":
        growth_accelerator(df),

        "Dividend Champion":
        dividend_champion(df),

        "Debt-Free Blue Chip":
        debt_free_bluechip(df),

        "Turnaround Watch":
        turnaround_watch(df)

    }



    for name,data in presets.items():

        print(
            name,
            ":",
            len(data),
            "companies"
        )


    with pd.ExcelWriter(
        "output/screener_output.xlsx"
    ) as writer:


        for name,data in presets.items():

            data.to_excel(
                writer,
                sheet_name=name[:31],
                index=False
            )


    print(
        "\nScreener report created successfully."
    )



if __name__=="__main__":

    main()