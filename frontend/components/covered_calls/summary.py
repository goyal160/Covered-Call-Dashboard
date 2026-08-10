import streamlit as st
import pandas as pd


def render_summary(open_df, closed_df):

    # =====================================================
    # SAFETY
    # =====================================================

    if open_df is None:
        open_df = pd.DataFrame()

    if closed_df is None:
        closed_df = pd.DataFrame()

    # Work on copies so the original API DataFrames
    # are not modified.
    open_df = open_df.copy()
    closed_df = closed_df.copy()

    # =====================================================
    # NUMERIC COLUMNS
    # =====================================================

    numeric_columns = [
        "sell_average",
        "buy_average",
        "quantity",
        "opening_charges",
        "closing_charges",
        "net_profit",
    ]

    for col in numeric_columns:

        if col in open_df.columns:

            open_df[col] = pd.to_numeric(
                open_df[col],
                errors="coerce",
            ).fillna(0)

        if col in closed_df.columns:

            closed_df[col] = pd.to_numeric(
                closed_df[col],
                errors="coerce",
            ).fillna(0)

    # =====================================================
    # COUNTS
    # =====================================================

    open_calls = len(open_df)

    closed_calls = len(closed_df)

    # =====================================================
    # OPEN CALL PREMIUM
    # =====================================================

    premium_collected = 0.0

    required_open_columns = {
        "sell_average",
        "quantity",
        "opening_charges",
    }

    if (
        not open_df.empty
        and required_open_columns.issubset(open_df.columns)
    ):

        premium_collected = (

            (
                open_df["sell_average"]
                * open_df["quantity"]
            )

            - open_df["opening_charges"]

        ).sum()

    # =====================================================
    # CLOSED CALL REALIZED PROFIT
    # =====================================================

    realized_profit = 0.0

    if (
        not closed_df.empty
        and "net_profit" in closed_df.columns
    ):

        realized_profit = (
            closed_df["net_profit"].sum()
        )

    # =====================================================
    # KPI CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Open Calls",
            open_calls,
        )

    with c2:

        st.metric(
            "Closed Calls",
            closed_calls,
        )

    with c3:

        st.metric(
            "Premium Collected",
            f"₹ {premium_collected:,.2f}",
        )

    with c4:

        st.metric(
            "Realized Profit",
            f"₹ {realized_profit:,.2f}",
        )