import streamlit as st
import pandas as pd
from datetime import date

from api import (
    get_dividends,
    create_dividend,
    delete_dividend,
    get_cash_holdings,
    is_logged_in,
)

from components.login import render_login
from components.sidebar import render_sidebar


# =====================================================
# AUTH
# =====================================================

if not is_logged_in():

    render_login()

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

render_sidebar(
    st.session_state["username"],
    show_dashboard=True,
)


# =====================================================
# PAGE
# =====================================================

st.title("💰 Dividend Management")

st.divider()


# =====================================================
# LOAD DATA
# =====================================================

holdings = get_cash_holdings()

dividends = get_dividends()

if holdings is None:
    holdings = pd.DataFrame()

if dividends is None:
    dividends = pd.DataFrame()


# =====================================================
# ADD DIVIDEND
# =====================================================

st.subheader("➕ Add Dividend")

if not holdings.empty:

    open_holdings = holdings.copy()

    if "status" in open_holdings.columns:

        open_holdings = open_holdings[
            open_holdings["status"] == "OPEN"
        ]

    holding_map = {

        row["script_name"]: row["id"]

        for _, row in open_holdings.iterrows()

    }

    with st.form("add_dividend_form"):

        selected_holding = st.selectbox(
            "Holding",
            list(holding_map.keys())
        )

        dividend_date = st.date_input(
            "Dividend Date",
            value=date.today()
        )

        amount = st.number_input(
            "Dividend Amount",
            min_value=0.0,
            step=100.0,
        )

        submitted = st.form_submit_button(
            "Add Dividend"
        )

        if submitted:

            payload = {

                "holding":
                    holding_map[selected_holding],

                "dividend_date":
                    str(dividend_date),

                "amount":
                    amount,
            }

            result = create_dividend(payload)

            if result:

                st.success(
                    "Dividend added successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Unable to add dividend."
                )

else:

    st.info(
        "No holdings available."
    )


st.divider()


# =====================================================
# DIVIDEND HISTORY
# =====================================================

st.subheader("📋 Dividend History")

if dividends.empty:

    st.info(
        "No dividends recorded."
    )

else:

    display = dividends.copy()

    columns = [

        "id",
        "dividend_date",
        "holding_name",
        "amount",
    ]

    display = display[columns]

    display.rename(
        columns={
            "dividend_date":
                "Date",

            "holding_name":
                "Holding",

            "amount":
                "Amount",
        },
        inplace=True,
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("🗑 Delete Dividend")

    delete_map = {

        f"{row['holding_name']} | "
        f"{row['dividend_date']} | "
        f"₹{row['amount']}":

        row["id"]

        for _, row in dividends.iterrows()
    }

    selected = st.selectbox(
        "Select Dividend",
        list(delete_map.keys())
    )

    if st.button("Delete Dividend"):

        dividend_id = delete_map[selected]

        result = delete_dividend(
            dividend_id
        )

        if result:

            st.success(
                "Dividend deleted."
            )

            st.rerun()

        else:

            st.error(
                "Unable to delete dividend."
            )