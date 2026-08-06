# import streamlit as st

# from api import create_cash_transaction


# def render_cash_transaction_form():

#     with st.expander(
#         "💳 Deposit / Withdraw Cash",
#         expanded=False,
#     ):

#         transaction_type = st.selectbox(
#             "Transaction",
#             [
#                 "DEPOSIT",
#                 "WITHDRAW",
#             ],
#         )

#         amount = st.number_input(
#             "Amount",
#             min_value=0.0,
#             step=100.0,
#         )

#         remarks = st.text_input(
#             "Remarks",
#         )

#         if st.button(
#             "Save Transaction",
#             use_container_width=True,
#         ):

#             create_cash_transaction(
#                 transaction_type,
#                 amount,
#                 remarks,
#             )

#             st.success(
#                 "Transaction Saved."
#             )

#             st.rerun()

import streamlit as st

from api import (
    create_cash_transaction,
    get_cash_balance,
)


def render_cash_transaction_form():

    with st.expander(
        "💳 Deposit / Withdraw Cash",
        expanded=False,
    ):

        # ------------------------------------
        # Current Cash Balance
        # ------------------------------------

        cash_balance = get_cash_balance()

        st.metric(
            "Current Cash Balance",
            f"₹ {cash_balance:,.2f}",
        )

        # ------------------------------------
        # Transaction Form
        # ------------------------------------

        with st.form(
            "cash_transaction_form",
            clear_on_submit=True,
        ):

            transaction_type = st.radio(
                "Transaction",
                [
                    "DEPOSIT",
                    "WITHDRAW",
                ],
                horizontal=True,
            )

            amount = st.number_input(
                "Amount",
                min_value=0.01,
                step=100.00,
                format="%.2f",
            )

            remarks = st.text_input(
                "Remarks",
            )

            submitted = st.form_submit_button(
                "Save Transaction",
                use_container_width=True,
            )

        if not submitted:
            return

        # ------------------------------------
        # Validation
        # ------------------------------------

        if (
            transaction_type == "WITHDRAW"
            and amount > cash_balance
        ):

            st.error(
                "Withdrawal amount exceeds available cash balance."
            )

            return

        # ------------------------------------
        # Save Transaction
        # ------------------------------------

        try:

            create_cash_transaction(
                transaction_type,
                amount,
                remarks,
            )

            st.success(
                "Transaction saved successfully."
            )

            st.cache_data.clear()

            st.rerun()

        except Exception as exc:

            st.error(
                f"Unable to save transaction.\n\n{exc}"
            )