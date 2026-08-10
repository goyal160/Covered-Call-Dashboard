import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar
from components.login import render_login

from components.kpi_cards import (
    dashboard_kpi_cards,
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
    cash_holding_summary_table,
    covered_call_summary_table,
)

from components.navigation import (
    quick_navigation,
    section_header,
)

from services import (
    portfolio_summary,
    dashboard_summary,
)

from components.styles import load_css


load_css()


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="My Dashboard",
    page_icon="📈",
    layout="wide",
)


# =====================================================
# AUTHENTICATION
# =====================================================

if not is_logged_in():

    render_login()

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

render_sidebar(
    st.session_state["username"]
)


st.title("📈 Portfolio Dashboard")

st.markdown("--")


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
# OPEN CASH HOLDINGS
# =====================================================

if (
    not cash.empty
    and
    "status" in cash.columns
):

    open_cash = cash[
        cash["status"]
        .astype(str)
        .str.upper()
        == "OPEN"
    ].copy()

else:

    open_cash = cash.copy()


# =====================================================
# PORTFOLIO SUMMARY
# =====================================================

summary = portfolio_summary(
    cash,
    calls,
)


# =====================================================
# ADDITIONAL DASHBOARD SUMMARY
# =====================================================

dashboard = dashboard_summary(
    cash,
    calls,
)


# =====================================================
# DASHBOARD OVERVIEW
# =====================================================

left, right = st.columns(
    [1.8, 1.2],
    gap="small",
)


with left:

    dashboard_kpi_cards(
        summary,
        dashboard,
    )


with right:

    portfolio_allocation_chart(
        open_cash
    )


st.divider()


# =====================================================
# CASH HOLDING SUMMARY
# =====================================================

st.subheader(
    "💰 Cash Holding Summary"
)

cash_holding_summary_table(
    cash
)


st.divider()


# =====================================================
# COVERED CALL SUMMARY
# =====================================================

st.subheader(
    "📞 Covered Call Summary"
)

covered_call_summary_table(
    calls
)


st.divider()


# =====================================================
# PORTFOLIO CASH
# =====================================================

st.subheader(
    "💵 Portfolio Cash"
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Available Cash",
        f"₹ {summary['cash_balance']:,.2f}",
    )


with c2:

    st.metric(
        "Total Deposits",
        f"₹ {summary['cash_added']:,.2f}",
    )


with c3:

    st.metric(
        "Total Withdrawals",
        f"₹ {summary['cash_withdrawn']:,.2f}",
    )


st.divider()


# =====================================================
# QUICK NAVIGATION
# =====================================================

quick_navigation()


st.divider()


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Covered Call Portfolio Management System | Phase 2 Dashboard"
)