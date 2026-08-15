import streamlit as st
from datetime import date

from api import create_dividend


def render_add_dividend_form(holdings_df):

    st.subheader("Add Dividend")

    if holdings_df is None or holdings_df.empty:

        st.info(
            "Add a cash holding first before recording a dividend."
        )

        return

    if "id" not in holdings_df.columns:

        st.error(
            "Holding information is unavailable."
        )

        return

    holdings = holdings_df.copy()

    holdings["id"] = holdings["id"].astype(int)

    script_options = holdings[
        ["id", "script_name"]
    ].drop_duplicates()

    script_options = script_options.sort_values(
        "script_name"
    )

    with st.form("add_dividend_form"):

        selected_script = st.selectbox(
            "Script",
            options=script_options["script_name"].tolist(),
        )

        dividend_amount = st.number_input(
            "Dividend Amount",
            min_value=0.01,
            step=0.01,
            format="%.2f",
        )

        dividend_date = st.date_input(
            "Dividend Date",
            value=date.today(),
        )

        submitted = st.form_submit_button(
            "Add Dividend",
            use_container_width=True,
        )

        if submitted:

            holding_id = int(
                script_options.loc[
                    script_options["script_name"]
                    == selected_script,
                    "id",
                ].iloc[0]
            )

            payload = {

                "holding": holding_id,

                "dividend_date": str(
                    dividend_date
                ),

                "amount": float(
                    dividend_amount
                ),

            }

            try:

                create_dividend(payload)

                st.success(
                    f"Dividend of ₹{dividend_amount:,.2f} "
                    f"added for {selected_script}."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to add dividend: {e}"
                )