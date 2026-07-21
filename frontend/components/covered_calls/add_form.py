import streamlit as st
from datetime import date

from api import create_covered_call


def render_add_form(holdings_df):

    with st.expander(
        "➕ Sell New Covered Call",
        expanded=False,
    ):

        if holdings_df.empty:

            st.warning(
                "Please create a Cash Holding first."
            )

            return

        with st.form("new_covered_call"):

            holding_name = st.selectbox(
                "Holding",
                holdings_df["script_name"].tolist(),
            )

            col1, col2 = st.columns(2)

            with col1:

                trade_date = st.date_input(
                    "Trade Date",
                    value=date.today(),
                )

                expiry_date = st.date_input(
                    "Expiry Date"
                )

                strike = st.number_input(
                    "Strike",
                    min_value=0.0,
                    format="%.2f",
                )

            with col2:

                sell_average = st.number_input(
                    "Sell Average",
                    min_value=0.0,
                    format="%.2f",
                )

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    step=1,
                )

                charges = st.number_input(
                    "Charges",
                    min_value=0.0,
                    format="%.2f",
                )

            submitted = st.form_submit_button(
                "Save Covered Call",
                use_container_width=True,
            )

        if not submitted:
            return

        holding_id = int(

            holdings_df.loc[
                holdings_df["script_name"] == holding_name,
                "id",
            ].iloc[0]

        )

        create_covered_call(

            {

                "holding": holding_id,

                "trade_date": str(trade_date),

                "expiry_date": str(expiry_date),

                "strike": strike,

                "sell_average": sell_average,

                "buy_average": 0,

                "quantity": quantity,

                "charges": charges,

                "status": "OPEN",

            }

        )

        st.success(
            "Covered Call Added Successfully."
        )

        st.cache_data.clear()

        st.rerun()