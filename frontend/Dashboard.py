import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from api import (
    get_cash_holdings,
    get_covered_calls,
)

from services import portfolio_summary


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Covered Call Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Covered Call Portfolio Dashboard")

st.markdown("---")


# =====================================================
# LOAD DATA
# =====================================================

cash = get_cash_holdings()

calls = get_covered_calls()


# =====================================================
# SAFETY
# =====================================================

if cash is None:
    cash = pd.DataFrame()

if calls is None:
    calls = pd.DataFrame()


# =====================================================
# PORTFOLIO SUMMARY
# =====================================================

summary = portfolio_summary(
    cash,
    calls
)


# =====================================================
# ADDITIONAL KPI CALCULATIONS
# =====================================================

total_holdings = len(cash)

open_calls = 0

closed_calls = 0

premium_collected = 0

total_charges = 0

if not calls.empty:

    if "status" in calls.columns:

        open_calls = len(
            calls[
                calls["status"] == "OPEN"
            ]
        )

        closed_calls = len(
            calls[
                calls["status"] == "CLOSED"
            ]
        )

    if (
        "sell_average" in calls.columns
        and
        "quantity" in calls.columns
    ):

        premium_collected = (
            calls.loc[
            calls["status"] == "OPEN",
            "sell_average"
            ]
            *
            calls.loc[
                calls["status"] == "OPEN",
                "quantity"
            ]
        ).sum()

    if "charges" in calls.columns:

        total_charges += calls[
            "charges"
        ].sum()

if (
    not cash.empty
    and
    "charges" in cash.columns
):

    total_charges += cash[
        "charges"
    ].sum()


# =====================================================
# KPI ROW - 1
# =====================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(

    "Investment",

    f"₹ {summary['investment']:,.2f}"

)

k2.metric(

    "Current Value",

    f"₹ {summary['current_value']:,.2f}"

)

k3.metric(

    "Equity Gain",

    f"₹ {summary['equity_gain']:,.2f}"

)

k4.metric(

    "ROI",

    f"{summary['roi']:.2f}%"

)


# =====================================================
# KPI ROW - 2
# =====================================================

k5, k6, k7, k8 = st.columns(4)

k5.metric(

    "Option Profit",

    f"₹ {summary['option_profit']:,.2f}"

)

k6.metric(

    "Open Calls",

    open_calls

)

k7.metric(

    "Closed Calls",

    closed_calls

)

k8.metric(

    "Holdings",

    total_holdings

)


# =====================================================
# KPI ROW - 3
# =====================================================

k9, k10 = st.columns(2)

k9.metric(

    "Premium Collected",

    f"₹ {premium_collected:,.2f}"

)

k10.metric(

    "Total Charges",

    f"₹ {total_charges:,.2f}"

)


st.divider()

# =====================================================
# PORTFOLIO ALLOCATION
# =====================================================

st.subheader("📊 Portfolio Allocation")

if cash.empty:

    st.info("No Cash Holdings Available.")

else:

    allocation = cash.copy()

    allocation["Holding Value"] = (
        allocation["current_price"]
        *
        allocation["quantity"]
    )

    fig = px.pie(

        allocation,

        names="script_name",

        values="Holding Value",

        hole=0.45,

        title="Portfolio Allocation"

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    st.plotly_chart(

        fig,

        width="stretch"

    )


st.divider()


# =====================================================
# TOP PERFORMING HOLDINGS
# =====================================================

st.subheader("🏆 Top Performing Holdings")

if cash.empty:

    st.info("No Holdings Available.")

else:

    top = cash.copy()

    top = top.sort_values(

        by="gain_loss",

        ascending=False

    )

    display = top[

        [

            "script_name",

            "buy_average",

            "current_price",

            "quantity",

            "gain_loss",

        ]

    ]

    display.columns = [

        "Script",

        "Buy Avg",

        "Current Price",

        "Qty",

        "Gain/Loss",

    ]

    st.dataframe(

        display,

        hide_index=True,

        width="stretch"

    )


st.divider()


# =====================================================
# CASH HOLDINGS
# =====================================================

left, right = st.columns([8, 1])

with left:

    st.subheader("💰 Cash Holdings")

with right:

    st.page_link(

        "pages/Cash_Holdings.py",

        label="➕ Add",

        icon="➕",

    )

if cash.empty:

    st.info(

        "No Cash Holdings Available."

    )

else:

    holdings = cash.copy()

    holdings["Investment"] = (

        holdings["buy_average"]

        *

        holdings["quantity"]

    )

    holdings["Current Value"] = (

        holdings["current_price"]

        *

        holdings["quantity"]

    )

    holdings = holdings[

        [

            "script_name",

            "buy_average",

            "current_price",

            "quantity",

            "Investment",

            "Current Value",

            "gain_loss",

            "charges",

        ]

    ]

    holdings.columns = [

        "Script",

        "Buy Avg",

        "Current Price",

        "Qty",

        "Investment",

        "Current Value",

        "Gain/Loss",

        "Charges",

    ]

    st.dataframe(

        holdings,

        hide_index=True,

        width="stretch",

    )


st.divider()


# =====================================================
# QUICK NAVIGATION
# =====================================================

st.subheader("⚡ Quick Navigation")

c1, c2, c3 = st.columns(3)

with c1:

    st.page_link(

        "pages/Cash_Holdings.py",

        label="💰 Cash Holdings",

        icon="💰",

    )

with c2:

    st.page_link(

        "pages/Covered_Calls.py",

        label="📞 Covered Calls",

        icon="📞",

    )

with c3:
    st.markdown(
        "[⚙ Django Admin](http://127.0.0.1:8000/admin/)"
    )


st.divider()

# =====================================================
# OPEN COVERED CALLS
# =====================================================

left, right = st.columns([8, 1])

with left:
    st.subheader("📞 Open Covered Calls")

with right:
    st.page_link(
        "pages/Covered_Calls.py",
        label="Manage",
        icon="📞",
    )

if calls.empty:

    st.info("No Covered Calls Available.")

else:

    open_calls_df = calls.copy()

    if "status" in open_calls_df.columns:
        open_calls_df = open_calls_df[
            open_calls_df["status"] == "OPEN"
        ]

    if open_calls_df.empty:

        st.info("No Open Covered Calls.")

    else:

        display = open_calls_df.copy()

        columns = [
            "trade_date",
            "script_name",
            "strike",
            "sell_average",
            "quantity",
            "option_profit",
            "status",
        ]

        display = display[
            [c for c in columns if c in display.columns]
        ]

        rename = {
            "trade_date": "Trade Date",
            "script_name": "Script",
            "strike": "Strike",
            "sell_average": "Sell Avg",
            "quantity": "Qty",
            "option_profit": "Option P/L",
            "status": "Status",
        }

        display.rename(
            columns=rename,
            inplace=True
        )

        st.dataframe(
            display,
            width="stretch",
            hide_index=True,
        )

st.divider()

# =====================================================
# RECENT COVERED CALL ACTIVITY
# =====================================================

st.subheader("🕒 Recent Covered Call Activity")

if calls.empty:

    st.info("No Activity Available.")

else:

    recent = calls.copy()

    if "trade_date" in recent.columns:

        recent = recent.sort_values(
            "trade_date",
            ascending=False,
        )

    recent = recent.head(5)

    cols = [
        "trade_date",
        "script_name",
        "strike",
        "sell_average",
        "quantity",
        "status",
    ]

    recent = recent[
        [c for c in cols if c in recent.columns]
    ]

    recent.rename(
        columns={
            "trade_date": "Trade Date",
            "script_name": "Script",
            "strike": "Strike",
            "sell_average": "Premium",
            "quantity": "Qty",
            "status": "Status",
        },
        inplace=True,
    )

    st.dataframe(
        recent,
        width="stretch",
        hide_index=True,
    )

st.divider()

# =====================================================
# EXPIRING CALLS
# =====================================================

st.subheader("📅 Calls Expiring Within 30 Days")

if calls.empty:

    st.info("No Covered Calls Available.")

else:

    if (
        "expiry_date" in calls.columns
        and
        "status" in calls.columns
    ):

        expiry = calls.copy()

        expiry = expiry[
            expiry["status"] == "OPEN"
        ]

        expiry["expiry_date"] = pd.to_datetime(
            expiry["expiry_date"],
            errors="coerce",
        )

        today = pd.Timestamp.today().normalize()

        future = today + pd.Timedelta(days=30)

        expiry = expiry[
            (
                expiry["expiry_date"] >= today
            )
            &
            (
                expiry["expiry_date"] <= future
            )
        ]

        if expiry.empty:

            st.success(
                "No Calls Expiring Within 30 Days."
            )

        else:

            cols = [
                "expiry_date",
                "script_name",
                "strike",
                "quantity",
                "sell_average",
            ]

            expiry = expiry[
                [c for c in cols if c in expiry.columns]
            ]

            expiry.rename(
                columns={
                    "expiry_date": "Expiry",
                    "script_name": "Script",
                    "strike": "Strike",
                    "quantity": "Qty",
                    "sell_average": "Premium",
                },
                inplace=True,
            )

            st.dataframe(
                expiry,
                width="stretch",
                hide_index=True,
            )

st.divider()

# =====================================================
# CLOSED COVERED CALLS
# =====================================================

st.subheader("✅ Closed Covered Calls")

if calls.empty:

    st.info("No Covered Calls Available.")

else:

    closed = calls.copy()

    if "status" in closed.columns:

        closed = closed[
            closed["status"] == "CLOSED"
        ]

    if closed.empty:

        st.info("No Closed Covered Calls.")

    else:

        cols = [
            "trade_date",
            "script_name",
            "strike",
            "sell_average",
            "buy_average",
            "quantity",
            "option_profit",
            "close_date",
        ]

        closed = closed[
            [c for c in cols if c in closed.columns]
        ]

        closed.rename(
            columns={
                "trade_date": "Trade Date",
                "script_name": "Script",
                "strike": "Strike",
                "sell_average": "Sell Avg",
                "buy_average": "Buy Avg",
                "quantity": "Qty",
                "option_profit": "Net Profit",
                "close_date": "Close Date",
            },
            inplace=True,
        )

        st.dataframe(
            closed,
            width="stretch",
            hide_index=True,
        )

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Covered Call Portfolio Management System | Phase 2 Dashboard"
)