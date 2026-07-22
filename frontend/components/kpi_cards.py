import streamlit as st
from utils import money, percent

# =====================================================
# GENERIC KPI CARD
# =====================================================

def metric(
    title,
    value,
    delta=None,
):
    """
    Wrapper around Streamlit metric.
    Keeps all KPI cards consistent.
    """

    st.metric(
        label=title,
        value=value,
        delta=delta,
        border=True,
    )


# =====================================================
# DASHBOARD KPI CARD
# =====================================================

def dashboard_kpi_cards(summary, dashboard):

    # ----------------------------
    # Row 1
    # ----------------------------

    c1, c2 = st.columns(2)

    with c1:
        metric(
            "Investment",
            money(summary["investment"]),
        )

    with c2:
        metric(
            "Current Value",
            money(summary["current_value"]),
        )

    # ----------------------------
    # Row 2
    # ----------------------------

    c1, c2 = st.columns(2)

    with c1:
        metric(
            "Equity Gain",
            money(summary["equity_gain"]),
        )

    with c2:
        metric(
            "ROI",
            percent(summary["roi"]),
        )

    # ----------------------------
    # Row 3
    # ----------------------------

    c1, c2 = st.columns(2)

    with c1:
        metric(
            "Option Profit",
            money(summary["option_profit"]),
        )

    with c2:
        metric(
            "Premium Collected",
            money(summary["premium_collected"]),
        )

    # ----------------------------
    # Row 4
    # ----------------------------

    c1, c2 = st.columns(2)

    with c1:
        metric(
            "Total Charges",
            money(dashboard["total_charges"]),
        )

    with c2:
        metric(
            "Net Portfolio P/L",
            money(summary["net_portfolio_pl"]),
        )