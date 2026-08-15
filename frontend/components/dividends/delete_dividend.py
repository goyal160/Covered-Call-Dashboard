import streamlit as st

from api import delete_dividend


def render_delete_dividend(dividends_df):

    st.subheader("Delete Dividend")

    if dividends_df is None or dividends_df.empty:

        st.info(
            "No dividends available to delete."
        )

        return

    df = dividends_df.copy()

    if "id" not in df.columns:

        st.error(
            "Dividend ID is unavailable."
        )

        return

    options = {}

    for _, row in df.iterrows():

        script = row.get(
            "holding_name",
            "Unknown",
        )

        dividend_date = row.get(
            "dividend_date",
            "",
        )

        amount = row.get(
            "amount",
            0,
        )

        label = (
            f"{script} | "
            f"{dividend_date} | "
            f"₹{float(amount):,.2f}"
        )

        options[label] = int(
            row["id"]
        )

    selected = st.selectbox(
        "Select Dividend",
        options=list(options.keys()),
    )

    if st.button(
        "Delete Dividend",
        type="secondary",
        use_container_width=True,
    ):

        dividend_id = options[selected]

        try:

            delete_dividend(
                dividend_id
            )

            st.success(
                "Dividend deleted successfully."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to delete dividend: {e}"
            )