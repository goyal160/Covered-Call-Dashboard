import streamlit as st
import pandas as pd

from api import get_cash_transactions


def render_cash_ledger():

    st.subheader("Cash Balance Ledger")

    transactions = get_cash_transactions()

    if transactions is None or transactions.empty:

        st.info("No cash transactions found.")

        return

    ledger = transactions.copy()

    # -------------------------------------------------
    # Dates
    # -------------------------------------------------

    if "transaction_date" in ledger.columns:

        ledger["transaction_date"] = pd.to_datetime(
            ledger["transaction_date"],
            errors="coerce",
        )

        ledger["transaction_date"] = (
            ledger["transaction_date"]
            .dt.strftime("%d-%b-%Y")
        )

    # -------------------------------------------------
    # Numeric fields
    # -------------------------------------------------

    for column in [
        "amount",
        "running_balance",
    ]:

        if column in ledger.columns:

            ledger[column] = pd.to_numeric(
                ledger[column],
                errors="coerce",
            ).fillna(0)

    # -------------------------------------------------
    # Holding name
    # -------------------------------------------------

    if "holding_name" not in ledger.columns:

        if "holding" in ledger.columns:

            ledger["holding_name"] = (
                ledger["holding"]
                .astype(str)
            )

        else:

            ledger["holding_name"] = ""

    # -------------------------------------------------
    # Display columns
    # -------------------------------------------------

    columns = [
        "transaction_date",
        "transaction_type",
        "amount",
        "running_balance",
        "holding_name",
        "remarks",
    ]

    columns = [
        column
        for column in columns
        if column in ledger.columns
    ]

    ledger = ledger[columns]

    # -------------------------------------------------
    # Rename
    # -------------------------------------------------

    ledger = ledger.rename(
        columns={
            "transaction_date": "Date",
            "transaction_type": "Type",
            "amount": "Amount",
            "running_balance": "Running Balance",
            "holding_name": "Holding",
            "remarks": "Remarks",
        }
    )

    # -------------------------------------------------
    # Latest transaction first
    # -------------------------------------------------

    ledger = ledger.iloc[::-1].reset_index(
        drop=True
    )

    # -------------------------------------------------
    # Formatting
    # -------------------------------------------------

    if "Amount" in ledger.columns:

        ledger["Amount"] = ledger["Amount"].map(
            lambda x: f"₹ {x:,.2f}"
        )

    if "Running Balance" in ledger.columns:

        ledger["Running Balance"] = (
            ledger["Running Balance"].map(
                lambda x: f"₹ {x:,.2f}"
            )
        )

    st.dataframe(
        ledger,
        use_container_width=True,
        hide_index=True,
    )