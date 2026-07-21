import streamlit as st

from api import patch_covered_call


def render_close_position(row):
    """
    Render Close Position button and form.
    """

    if st.button(
        "✔ Close Position",
        key=f"close_{row['id']}",
        use_container_width=True,
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

        charges = st.number_input(
            "Closing Charges",
            min_value=0.0,
            value=float(row.get("charges", 0)),
            format="%.2f",
        )

        submitted = st.form_submit_button(
            "Close Position",
            use_container_width=True,
        )

    if not submitted:
        return

    patch_covered_call(

        row["id"],

        {

            "buy_average": buy_average,

            "charges": charges,

            "close_date": str(close_date),

            "status": "CLOSED",

        },

    )

    st.success(
        "Position Closed Successfully."
    )

    st.cache_data.clear()

    st.session_state["close_id"] = None

    st.rerun()