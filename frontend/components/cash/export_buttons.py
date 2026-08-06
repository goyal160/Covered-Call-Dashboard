from io import BytesIO

import pandas as pd
import streamlit as st


def render_export_buttons(display):

    csv = display.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📄 Download CSV",

        csv,

        "cash_holdings.csv",

        "text/csv",

        width="stretch",

    )

    try:

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:

            display.to_excel(
                writer,
                index=False,
            )

        st.download_button(

            "📊 Download Excel",

            output.getvalue(),

            "cash_holdings.xlsx",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            width="stretch",

        )

    except Exception:

        st.info(
            "Excel export unavailable."
        )