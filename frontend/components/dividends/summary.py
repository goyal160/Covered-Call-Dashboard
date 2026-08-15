import streamlit as st
import pandas as pd

from api import get_dividends


def render_dividend_summary():

    st.subheader("Dividend Income")

    dividends = get_dividends()

    if dividends is None or dividends.empty:

        st.info(
            "No dividends recorded yet."
        )

        return

    df = dividends.copy()

    if "amount" in df.columns:

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce",
        ).fillna(0)

    if "dividend_date" in df.columns:

        df["dividend_date"] = pd.to_datetime(
            df["dividend_date"],
            errors="coerce",
        ).dt.strftime("%d-%m-%Y")

    display_columns = [
        "holding_name",
        "dividend_date",
        "amount",
    ]

    available_columns = [
        col
        for col in display_columns
        if col in df.columns
    ]

    display_df = df[
        available_columns
    ].copy()

    display_df.rename(
        columns={
            "holding_name": "Script",
            "dividend_date": "Date",
            "amount": "Dividend",
        },
        inplace=True,
    )

    if "Dividend" in display_df.columns:

        display_df["Dividend"] = (
            display_df["Dividend"]
            .map(
                lambda x:
                f"₹{x:,.2f}"
            )
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )