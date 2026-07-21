import streamlit as st

from api import (
    patch_cash_holding,
    delete_cash_holding,
)


def render_edit_form(row):

    with st.form(f"edit_cash_{row['id']}"):

        buy = st.number_input(
            "Buy Average",
            value=float(row["buy_average"]),
            format="%.2f",
        )

        current = st.number_input(
            "Current Price",
            value=float(row["current_price"]),
            format="%.2f",
        )

        qty = st.number_input(
            "Quantity",
            value=int(row["quantity"]),
            min_value=1,
        )

        charges = st.number_input(
            "Charges",
            value=float(row["charges"]),
            format="%.2f",
        )

        submitted = st.form_submit_button(
            "Save Changes"
        )

        if submitted:

            patch_cash_holding(

                row["id"],

                {

                    "buy_average": buy,

                    "current_price": current,

                    "quantity": qty,

                    "charges": charges,

                },

            )

            st.success(
                "Holding Updated Successfully."
            )

            st.session_state["edit_cash"] = None

            st.rerun()

def render_delete_confirmation(row):

    st.warning(
        "Delete this holding?"
    )

    yes, no = st.columns(2)

    with yes:

        if st.button(
            "YES",
            key=f"yes_{row['id']}",
        ):

            delete_cash_holding(
                row["id"]
            )

            st.success(
                "Holding Deleted."
            )

            st.session_state["delete_cash"] = None

            st.rerun()

    with no:

        if st.button(
            "Cancel",
            key=f"cancel_{row['id']}",
        ):

            st.session_state["delete_cash"] = None

            st.rerun()

def render_holding_cards(cash_df):

    if cash_df.empty:

        st.info("No holdings available.")

        return

    for _, row in cash_df.iterrows():

        investment = (
            row["buy_average"]
            * row["quantity"]
        )

        current_value = (
            row["current_price"]
            * row["quantity"]
        )

        title = (
            f"📈 {row['script_name']} "
            f"| Qty : {int(row['quantity'])}"
        )

        with st.expander(title):

            left, right = st.columns(2)

            with left:

                st.write(
                    f"**Buy Average :** ₹ {row['buy_average']:,.2f}"
                )

                st.write(
                    f"**Current Price :** ₹ {row['current_price']:,.2f}"
                )

                st.write(
                    f"**Quantity :** {int(row['quantity'])}"
                )

                st.write(
                    f"**Investment :** ₹ {investment:,.2f}"
                )

            with right:

                st.write(
                    f"**Current Value :** ₹ {current_value:,.2f}"
                )

                st.write(
                    f"**Gain / Loss :** ₹ {row['gain_loss']:,.2f}"
                )

                st.write(
                    f"**Charges :** ₹ {row['charges']:,.2f}"
                )

            st.divider()

            edit_col, delete_col = st.columns(2)

            # =====================================================
            # EDIT BUTTON
            # =====================================================

            with edit_col:

                if st.button(
                    "✏ Edit",
                    key=f"edit_{row['id']}",
                ):

                    st.session_state["edit_cash"] = row["id"]

            if st.session_state.get("edit_cash") == row["id"]:

                render_edit_form(row)

            # =====================================================
            # DELETE BUTTON
            # =====================================================

            with delete_col:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{row['id']}",
                ):

                    st.session_state["delete_cash"] = row["id"]

            if st.session_state.get("delete_cash") == row["id"]:

                render_delete_confirmation(row)