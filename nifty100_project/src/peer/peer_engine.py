import sqlite3
import pandas as pd


DB = "db/nifty100.db"



def load_peer_data():

    conn = sqlite3.connect(DB)


    query = """

    SELECT

        pg.company_id,
        pg.peer_group_name,

        fr.year,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,

        fr.debt_to_equity,
        fr.free_cash_flow,

        fr.interest_coverage,
        fr.asset_turnover,

        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr


    FROM peer_groups pg


    LEFT JOIN financial_ratios fr

    ON pg.company_id = fr.company_id

    """


    df = pd.read_sql(query, conn)

    conn.close()


    return df




def calculate_percentile(series):

    return series.rank(
        pct=True,
        method="average"
    )




def create_peer_percentiles(df):


    metrics = {


        "ROE":
        "return_on_equity_pct",


        "ROCE":
        "return_on_capital_employed_pct",


        "NPM":
        "net_profit_margin_pct",


        "DE":
        "debt_to_equity",


        "FCF":
        "free_cash_flow",


        "PAT_CAGR":
        "pat_cagr_5yr",


        "Revenue_CAGR":
        "revenue_cagr_5yr",


        "EPS_CAGR":
        "eps_cagr_5yr",


        "ICR":
        "interest_coverage",


        "Asset_Turnover":
        "asset_turnover"

    }



    output=[]



    for peer, group in df.groupby(
        "peer_group_name"
    ):


        for metric,column in metrics.items():


            temp = group[
                [
                    "company_id",
                    "year",
                    column
                ]
            ].copy()



            temp=temp.dropna(
                subset=[column]
            )


            if len(temp)==0:
                continue



            # Lower debt is better
            if metric=="DE":

                temp["percentile_rank"] = (
                    1 -
                    calculate_percentile(
                        temp[column]
                    )
                )


            else:

                temp["percentile_rank"] = (
                    calculate_percentile(
                        temp[column]
                    )
                )



            for _,row in temp.iterrows():


                output.append({

                    "company_id":
                    row["company_id"],


                    "peer_group_name":
                    peer,


                    "metric":
                    metric,


                    "value":
                    row[column],


                    "percentile_rank":
                    row["percentile_rank"],


                    "year":
                    row["year"]

                })



    return pd.DataFrame(output)





def save_peer_percentiles(df):


    conn = sqlite3.connect(DB)


    df.to_sql(

        "peer_percentiles",

        conn,

        if_exists="replace",

        index=False

    )


    conn.close()




def main():


    print("Loading peer data...")


    df = load_peer_data()


    print(
        "Rows loaded:",
        len(df)
    )


    print(
        "Calculating peer percentiles..."
    )


    result = create_peer_percentiles(df)


    print(
        "Percentile rows:",
        len(result)
    )


    save_peer_percentiles(result)


    print(
        "peer_percentiles table created successfully"
    )




if __name__=="__main__":

    main()