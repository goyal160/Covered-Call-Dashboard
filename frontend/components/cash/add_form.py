import streamlit as st

from api import create_cash_holding


def render_add_holding():

    with st.expander("➕ Add Holding"):

        with st.form("cash_form"):

            c1, c2, c3 = st.columns(3)

            script = c1.text_input("Script Name")

            buy = c2.number_input(
                "Buy Average",
                min_value=0.0,
                format="%.2f",
            )

            current = c3.number_input(
                "Current Price",
                min_value=0.0,
                format="%.2f",
            )

            c4, c5 = st.columns(2)

            qty = c4.number_input(
                "Quantity",
                min_value=1,
                step=1,
            )

            charges = c5.number_input(
                "Charges",
                min_value=0.0,
                format="%.2f",
            )

            submitted = st.form_submit_button(
                "Add Holding",
                use_container_width=True,
            )

            if submitted:

                create_cash_holding({

                    "script_name": script,

                    "buy_average": buy,

                    "current_price": current,

                    "quantity": qty,

                    "charges": charges,

                })

                st.success("Holding Added.")

                st.rerun()