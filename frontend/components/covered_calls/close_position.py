import streamlit as st

from api import close_covered_call


def render_close_position(row):
    """
    Render Close Position button and form.
    """

    if st.button(
        "✔ Close Position",
        key=f"close_{row['id']}",
        width="stretch",
    ):
        st.session_state["close_id"] = row["id"]

    if st.session_state.get("close_id") != row["id"]:
        return

    with st.form(
        f"close_form_{row['id']}"
    ):

        buy_average = st.number_input(
            "Buy Average",
            min_value=0.0,
            value=float(row.get("buy_average", 0)),
            format="%.2f",
        )

        close_date = st.date_input(
            "Close Date"
        )

        closing_charges = st.number_input(
            "Closing Charges",
            min_value=0.0,
            value=0.0,
            format="%.2f",
        )

        submitted = st.form_submit_button(
            "Close Position",
            width="stretch",
        )

    if not submitted:
        return

    close_covered_call(
        row["id"],
        buy_average,
        close_date,
        closing_charges,
    )

    st.success(
        "Position Closed Successfully."
    )

    st.cache_data.clear()

    st.session_state["close_id"] = None

    st.rerun()