import streamlit as st

from components.covered_calls.edit_position import (
    render_edit_position,
)

from components.covered_calls.close_position import (
    render_close_position,
)

from components.covered_calls.delete_position import (
    render_delete_position,
)


def render_open_card(row):

    premium = (
        float(row["sell_average"])
        * int(row["quantity"])
    )

    title = (

        f"📌 {row['holding_name']}"

        f" | Strike {row['strike']}"

        f" | Qty {row['quantity']}"

    )

    with st.expander(title):

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

        with right:

            st.write("**Quantity**")
            st.write(row["quantity"])

            st.write("**Charges**")
            st.write(row["charges"])

            st.write("**Premium Collected**")
            st.write(f"₹ {premium:,.2f}")

            st.write("**Status**")
            st.success("OPEN")

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            render_edit_position(row)

        with c2:
            render_close_position(row)

        with c3:
            render_delete_position(row)