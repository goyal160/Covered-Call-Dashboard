import streamlit as st
import pandas as pd

from api import update_dividend


def render_edit_dividend(
    dividends_df,
    holdings_df,
):

    st.subheader("Edit Dividend")

    if dividends_df is None or dividends_df.empty:

        st.info(
            "No dividends available to edit."
        )

        return

    if holdings_df is None or holdings_df.empty:

        st.info(
            "No holdings available."
        )

        return

    df = dividends_df.copy()

    if "id" not in df.columns:

        st.error(
            "Dividend ID is unavailable."
        )

        return

    labels = {}

    for _, row in df.iterrows():

        label = (
            f"{row.get('holding_name', 'Unknown')} | "
            f"{row.get('dividend_date', '')} | "
            f"₹{float(row.get('amount', 0)):,.2f}"
        )

        labels[label] = row

    selected_label = st.selectbox(
        "Select Dividend",
        options=list(labels.keys()),
    )

    selected = labels[selected_label]

    holdings = holdings_df[
        ["id", "script_name"]
    ].drop_duplicates()

    holdings = holdings.sort_values(
        "script_name"
    )

    current_script = selected.get(
        "holding_name"
    )

    script_names = holdings[
        "script_name"
    ].tolist()

    default_index = 0

    if current_script in script_names:

        default_index = script_names.index(
            current_script
        )

    selected_script = st.selectbox(
        "Script",
        options=script_names,
        index=default_index,
    )

    current_date = pd.to_datetime(
        selected.get("dividend_date")
    ).date()

    current_amount = float(
        selected.get("amount", 0)
    )

    dividend_date = st.date_input(
        "Dividend Date",
        value=current_date,
    )

    dividend_amount = st.number_input(
        "Dividend Amount",
        min_value=0.01,
        value=current_amount,
        step=0.01,
        format="%.2f",
    )

    if st.button(
        "Update Dividend",
        use_container_width=True,
    ):

        holding_id = int(
            holdings.loc[
                holdings["script_name"]
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

            update_dividend(
                int(selected["id"]),
                payload,
            )

            st.success(
                "Dividend updated successfully."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to update dividend: {e}"
            )