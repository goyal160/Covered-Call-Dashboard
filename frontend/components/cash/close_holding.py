import streamlit as st
from datetime import date

from api import close_cash_holding


def render_close_holding(row):

    st.warning(
        f"You are about to close **{row['script_name']}**."
    )

    with st.form(f"close_cash_form_{row['id']}"):

        sell_price = st.number_input(
            "Sell Price",
            value=float(row["current_price"]),
            format="%.2f",
            min_value=0.01,
        )

        close_date = st.date_input(
            "Close Date",
            value=date.today(),
        )

        charges = st.number_input(
            "Closing Charges",
            value=0.00,
            min_value=0.00,
            format="%.2f",
        )

        # =====================================================
        # Closing Summary
        # =====================================================

        investment = (
            float(row["buy_average"])
            * int(row["quantity"])
        )

        sale_value = (
            sell_price
            * int(row["quantity"])
        )

        gross_profit = (
            sale_value
            - investment
        )

        total_charges = (
            float(row["charges"])
            + charges
        )

        net_profit = (
            gross_profit
            - total_charges
        )

        st.divider()

        st.markdown("### Closing Summary")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Investment",
                f"₹ {investment:,.2f}",
            )

            st.metric(
                "Sale Value",
                f"₹ {sale_value:,.2f}",
            )

        with c2:

            st.metric(
                "Gross Profit",
                f"₹ {gross_profit:,.2f}",
            )

            st.metric(
                "Net Realized Profit",
                f"₹ {net_profit:,.2f}",
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            submit = st.form_submit_button(
                "✅ Close Holding"
            )

        with col2:

            cancel = st.form_submit_button(
                "Cancel"
            )

    # =====================================================
    # Cancel
    # =====================================================

    if cancel:

        st.session_state["close_cash"] = None

        st.rerun()

    # =====================================================
    # Submit
    # =====================================================

    if submit:

        if sell_price <= 0:

            st.error(
                "Sell price must be greater than zero."
            )

            st.stop()

        if charges < 0:

            st.error(
                "Charges cannot be negative."
            )

            st.stop()

        try:

            close_cash_holding(

                row["id"],

                sell_price,

                close_date,

                charges,

            )

            st.success(
                f"{row['script_name']} closed successfully."
            )

            st.session_state["close_cash"] = None

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to close holding.\n\n{e}"
            )