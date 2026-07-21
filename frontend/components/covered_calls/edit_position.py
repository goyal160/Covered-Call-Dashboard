import streamlit as st
import pandas as pd

from api import patch_covered_call


# ============================================================
# EDIT OPEN POSITION
# ============================================================

def render_edit_position(row):

    if st.button(
        "✏ Edit",
        key=f"edit_{row['id']}",
        use_container_width=True,
    ):
        st.session_state["edit_id"] = row["id"]

    if st.session_state.get("edit_id") != row["id"]:
        return

    with st.form(
        f"edit_form_{row['id']}"
    ):

        strike = st.number_input(
            "Strike",
            value=float(row["strike"]),
            format="%.2f",
        )

        sell_average = st.number_input(
            "Sell Average",
            value=float(row["sell_average"]),
            format="%.2f",
        )

        quantity = st.number_input(
            "Quantity",
            value=int(row["quantity"]),
            min_value=1,
            step=1,
        )

        charges = st.number_input(
            "Charges",
            value=float(row["charges"]),
            format="%.2f",
        )

        save = st.form_submit_button(
            "Save Changes",
            use_container_width=True,
        )

    if not save:
        return

    patch_covered_call(
        row["id"],
        {
            "strike": strike,
            "sell_average": sell_average,
            "quantity": quantity,
            "charges": charges,
        },
    )

    st.success(
        "Position Updated Successfully."
    )

    st.cache_data.clear()

    st.session_state["edit_id"] = None

    st.rerun()


# ============================================================
# EDIT CLOSED POSITION
# ============================================================

def render_edit_closed_position(row):

    if st.button(
        "✏ Edit",
        key=f"edit_closed_{row['id']}",
        use_container_width=True,
    ):
        st.session_state["edit_closed_id"] = row["id"]

    if (
        st.session_state.get("edit_closed_id")
        != row["id"]
    ):
        return

    with st.form(
        f"edit_closed_form_{row['id']}"
    ):

        strike = st.number_input(
            "Strike",
            value=float(row["strike"]),
            format="%.2f",
        )

        sell_average = st.number_input(
            "Sell Average",
            value=float(row["sell_average"]),
            format="%.2f",
        )

        buy_average = st.number_input(
            "Buy Average",
            value=float(row["buy_average"]),
            format="%.2f",
        )

        quantity = st.number_input(
            "Quantity",
            value=int(row["quantity"]),
            min_value=1,
            step=1,
        )

        charges = st.number_input(
            "Charges",
            value=float(row["charges"]),
            format="%.2f",
        )

        close_date = st.date_input(
            "Close Date",
            value=pd.to_datetime(
                row["close_date"]
            ).date(),
        )

        save = st.form_submit_button(
            "Save Changes",
            use_container_width=True,
        )

    if not save:
        return

    patch_covered_call(
        row["id"],
        {
            "strike": strike,
            "sell_average": sell_average,
            "buy_average": buy_average,
            "quantity": quantity,
            "charges": charges,
            "close_date": str(close_date),
        },
    )

    st.success(
        "Closed Position Updated Successfully."
    )

    st.cache_data.clear()

    st.session_state["edit_closed_id"] = None

    st.rerun()