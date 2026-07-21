import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from components.sidebar import render_sidebar
from components.login import render_login

from components.kpi_cards import (
    portfolio_summary_cards,
    option_summary_cards,
    charges_cards,
)

from components.charts import (
    portfolio_allocation_chart,
)

from api import (
    is_logged_in,
    get_cash_holdings,
    get_covered_calls,
)

from components.tables import (
    cash_holdings_table,
    open_calls_table,
    recent_activity_table,
    closed_calls_table,
)

from components.navigation import quick_navigation, section_header

from services import (
    portfolio_summary,
    dashboard_summary,
)

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Covered Call Dashboard",
    page_icon="📈",
    layout="wide",
)

if not is_logged_in():

    render_login()

    st.stop()

render_sidebar(
    st.session_state["username"]
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

dashboard = dashboard_summary(
    cash,
    calls,
)

portfolio_summary_cards(summary)

option_summary_cards(
    summary["option_profit"],
    dashboard["open_calls"],
    dashboard["closed_calls"],
    dashboard["total_holdings"],
)

charges_cards(
    dashboard["premium_collected"],
    dashboard["total_charges"],
)

# =====================================================
# PORTFOLIO ALLOCATION
# =====================================================

portfolio_allocation_chart(cash)

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

section_header(
    "💰 Cash Holdings",
    "pages/Cash_Holdings.py",
    "➕ Add",
    "➕",
)

if cash.empty:

    st.info(

        "No Cash Holdings Available."

    )

else:

    cash_holdings_table(cash)


st.divider()


# =====================================================
# QUICK NAVIGATION
# =====================================================

quick_navigation()

st.divider()

# =====================================================
# OPEN COVERED CALLS
# =====================================================

section_header(
    "📞 Open Covered Calls",
    "pages/Covered_Calls.py",
    "Manage",
    "📞",
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

        open_calls_table(open_calls_df)

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

    recent_activity_table(recent)

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

        closed_calls_table(closed)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Covered Call Portfolio Management System | Phase 2 Dashboard"
)