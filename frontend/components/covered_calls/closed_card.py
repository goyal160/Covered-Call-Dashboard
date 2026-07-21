import streamlit as st

from components.covered_calls.edit_position import (
    render_edit_closed_position,
)

from components.covered_calls.delete_position import (
    render_delete_closed_position,
)


def render_closed_card(row):
    """
    Render one closed covered call card.
    """

    holding = row.get(
        "holding_name",
        row.get("script_name", "Holding"),
    )

    title = (
        f"✅ {holding}"
        f" | Strike {row['strike']}"
        f" | Qty {row['quantity']}"
    )

    with st.expander(
        title,
        expanded=False,
    ):

        left, right = st.columns(2)

        with left:

            st.write("**Trade Date**")
            st.write(row["trade_date"])

            st.write("**Expiry Date**")
            st.write(row["expiry_date"])

            st.write("**Strike**")
            st.write(row["strike"])

            st.write("**Sell Average**")
            st.write(row["sell_average"])

            st.write("**Buy Average**")
            st.write(row["buy_average"])

        with right:

            st.write("**Quantity**")
            st.write(row["quantity"])

            st.write("**Charges**")
            st.write(row["charges"])

            st.write("**Close Date**")
            st.write(row["close_date"])

            st.write("**Net Profit**")
            st.success(
                f"₹ {float(row['net_profit']):,.2f}"
            )

            st.write("**Status**")
            st.success("CLOSED")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            render_edit_closed_position(row)

        with c2:
            render_delete_closed_position(row)