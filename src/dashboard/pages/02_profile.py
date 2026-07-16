import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_company_summary,
    get_pros_cons,
)


# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
    layout="wide"
)


# -----------------------------------------------------
# Title
# -----------------------------------------------------

st.title("🏢 Company Profile")


# -----------------------------------------------------
# Load Companies
# -----------------------------------------------------

companies = get_companies()

if companies.empty:
    st.error("No company data available.")
    st.stop()


options = companies["id"].tolist()

ticker = st.selectbox(
    "Select Company",
    options
)


if not ticker:
    st.warning("Ticker not found.")
    st.stop()



# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

company = companies[
    companies["id"] == ticker
].iloc[0]


ratios = get_ratios(ticker)

pl = get_pl(ticker)

summary = get_company_summary(ticker)

pros_cons = get_pros_cons(ticker)



# -----------------------------------------------------
# Company Information
# -----------------------------------------------------

st.subheader(company["company_name"])


col1, col2 = st.columns(2)


with col1:

    st.write(
        f"**Ticker:** {company['id']}"
    )

    st.write(
        f"**Website:** {company['website']}"
    )


with col2:

    st.write("**About Company**")

    st.write(
        company["about_company"]
    )



# -----------------------------------------------------
# Financial Metrics
# -----------------------------------------------------

if not ratios.empty:


    latest = (
        ratios
        .sort_values("year")
        .iloc[-1]
    )


    st.subheader("📊 Key Financial Metrics")


    c1, c2, c3 = st.columns(3)

    c1.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

    c2.metric(
        "ROCE",
        f"{latest['return_on_capital_employed_pct']:.2f}%"
    )

    c3.metric(
        "Net Profit Margin",
        f"{latest['net_profit_margin_pct']:.2f}%"
    )



    c4, c5, c6 = st.columns(3)


    c4.metric(
        "Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
    )


    c5.metric(
        "Revenue CAGR (5Y)",
        f"{latest['revenue_cagr_5yr']:.2f}%"
    )


    c6.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow']:.2f}"
    )


else:

    st.info(
        "Financial ratios not available."
    )



# -----------------------------------------------------
# Revenue and Profit Chart
# -----------------------------------------------------

if not pl.empty:


    pl = pl.sort_values("year")


    st.subheader(
        "📈 Revenue vs Net Profit"
    )


    fig = px.bar(

        pl,

        x="year",

        y=[
            "sales",
            "net_profit"
        ],

        barmode="group",

        title="Revenue and Profit Trend"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# -----------------------------------------------------
# ROE ROCE Trend
# -----------------------------------------------------

if not ratios.empty:


    st.subheader(
        "📉 ROE vs ROCE Trend"
    )


    fig2 = px.line(

        ratios.sort_values("year"),

        x="year",

        y=[
            "return_on_equity_pct",
            "return_on_capital_employed_pct"
        ],

        markers=True,

        title="Return Efficiency Trend"

    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



# -----------------------------------------------------
# AI Company Summary
# -----------------------------------------------------

st.subheader(
    "🤖 AI Company Summary"
)


if not summary.empty:


    st.success(
        summary.iloc[0]["summary"]
    )


else:

    st.info(
        "AI summary not generated."
    )



# -----------------------------------------------------
# Pros & Cons
# -----------------------------------------------------

st.subheader(
    "⚖️ Investment Pros & Cons"
)



if not pros_cons.empty:


    col1, col2 = st.columns(2)



    with col1:

        st.markdown(
            "### ✅ Strengths"
        )


        pros = pros_cons[
            pros_cons["type"] == "Pro"
        ]


        if pros.empty:

            st.write(
                "No strengths identified."
            )

        else:

            for _, row in pros.iterrows():

                st.success(
                    f"{row['text']} "
                    f"(Confidence: {row['confidence_pct']}%)"
                )



    with col2:

        st.markdown(
            "### ⚠️ Risks"
        )


        cons = pros_cons[
            pros_cons["type"] == "Con"
        ]


        if cons.empty:

            st.write(
                "No major risks identified."
            )

        else:

            for _, row in cons.iterrows():

                st.error(
                    f"{row['text']} "
                    f"(Confidence: {row['confidence_pct']}%)"
                )


else:

    st.info(
        "Pros & Cons data not available."
    )