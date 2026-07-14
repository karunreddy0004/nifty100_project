import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl,
)

st.set_page_config(page_title="Company Profile", page_icon="🏢", layout="wide")

st.title("🏢 Company Profile")

companies = get_companies()

options = companies["id"].tolist()
ticker = st.selectbox("Select Company", options)

if not ticker:
    st.warning("Ticker not found — please try another.")
    st.stop()

company = companies[companies["id"] == ticker].iloc[0]
ratios = get_ratios(ticker)
pl = get_pl(ticker)

st.subheader(company["company_name"])

col1, col2 = st.columns(2)
with col1:
    st.write(f"**Ticker:** {company['id']}")
    st.write(f"**Website:** {company['website']}")
with col2:
    st.write("**About Company**")
    st.write(company["about_company"])

if ratios.empty:
    st.info("Financial ratios not available.")
else:
    latest = ratios.sort_values("year").iloc[-1]

    c1, c2, c3 = st.columns(3)
    c1.metric("ROE", f"{latest['return_on_equity_pct']:.2f}%")
    c2.metric("ROCE", f"{latest['return_on_capital_employed_pct']:.2f}%")
    c3.metric("Net Profit Margin", f"{latest['net_profit_margin_pct']:.2f}%")

    c4, c5, c6 = st.columns(3)
    c4.metric("Debt / Equity", f"{latest['debt_to_equity']:.2f}")
    c5.metric("Revenue CAGR (5Y)", f"{latest['revenue_cagr_5yr']:.2f}%")
    c6.metric("Free Cash Flow", f"{latest['free_cash_flow']:.2f}")

if not pl.empty:
    pl = pl.sort_values("year")

    st.subheader("Revenue vs Net Profit")

    fig = px.bar(
        pl,
        x="year",
        y=["sales", "net_profit"],
        barmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)

if not ratios.empty:
    st.subheader("ROE vs ROCE")

    fig2 = px.line(
        ratios.sort_values("year"),
        x="year",
        y=[
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
        ],
        markers=True,
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Pros & Cons")
st.info("Pros & Cons data not available in the current database.")
