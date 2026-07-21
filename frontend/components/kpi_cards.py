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

    st.metric(
        label=title,
        value=value,
        delta=delta,
    )


# =====================================================
# PORTFOLIO SUMMARY KPIs
# =====================================================

def portfolio_summary_cards(summary):

    c1, c2, c3, c4 = st.columns(4)

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

    with c3:
        metric(
            "Equity Gain",
            money(summary["equity_gain"]),
        )

    with c4:
        metric(
            "ROI",
            percent(summary["roi"]),
        )


# =====================================================
# OPTION SUMMARY KPIs
# =====================================================

def option_summary_cards(

    option_profit,
    open_calls,
    closed_calls,
    holdings,

):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric(
            "Option Profit",
            money(option_profit),
        )

    with c2:
        metric(
            "Open Calls",
            open_calls,
        )

    with c3:
        metric(
            "Closed Calls",
            closed_calls,
        )

    with c4:
        metric(
            "Holdings",
            holdings,
        )


# =====================================================
# CHARGES KPIs
# =====================================================

def charges_cards(

    premium_collected,
    total_charges,

):

    c1, c2 = st.columns(2)

    with c1:
        metric(
            "Premium Collected",
            money(premium_collected),
        )

    with c2:
        metric(
            "Total Charges",
            money(total_charges),
        )