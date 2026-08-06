import streamlit as st
import pandas as pd


def render_summary(open_df, closed_df):

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

    open_calls = len(open_df)

    closed_calls = len(closed_df)

    premium_collected = 0.0

    realized_profit = 0.0

    # ----------------------------------------
    # Premium Collected
    # ----------------------------------------

    if not open_df.empty:

        premium_collected = (
            (
                open_df["sell_average"]
                * open_df["quantity"]
            )
            - open_df["opening_charges"]
        ).sum()

    # ----------------------------------------
    # Realized Profit
    # ----------------------------------------

    if (

        not closed_df.empty

        and

        "net_profit" in closed_df.columns

    ):

        realized_profit = (

            closed_df["net_profit"]

            .fillna(0)

            .sum()

        )

    # ----------------------------------------
    # KPI CARDS
    # ----------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Open Calls",

        open_calls,

    )

    c2.metric(

        "Closed Calls",

        closed_calls,

    )

    c3.metric(

        "Premium Collected",

        f"₹ {premium_collected:,.2f}",

    )

    c4.metric(

        "Realized Profit",

        f"₹ {realized_profit:,.2f}",

    )