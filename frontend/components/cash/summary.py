import streamlit as st


def render_cash_summary(summary: dict):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Holdings",
        summary["total_holdings"],
    )

    c2.metric(
        "Investment",
        f"₹ {summary['investment']:,.2f}",
    )

    c3.metric(
        "Current Value",
        f"₹ {summary['current_value']:,.2f}",
    )

    c4.metric(
        "Gain / Loss",
        f"₹ {summary['gain_loss']:,.2f}",
    )