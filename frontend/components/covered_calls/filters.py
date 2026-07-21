import streamlit as st
import pandas as pd


SORT_OPTIONS = [
    "Trade Date",
    "Expiry",
    "Strike",
    "Premium",
    "Quantity",
]


def filter_open_calls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Search + Sort Open Covered Calls.

    Returns filtered dataframe.
    """

    if df.empty:
        return df

    left, right = st.columns([3, 1])

    with left:
        search = st.text_input(
            "🔍 Search Holding",
            key="open_call_search",
        )

    with right:
        sort_by = st.selectbox(
            "Sort By",
            SORT_OPTIONS,
            key="open_call_sort",
        )

    result = df.copy()

    # ----------------------------------------
    # Search
    # ----------------------------------------

    if (
        search
        and "script_name" in result.columns
    ):

        result = result[
            result["script_name"].str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    # ----------------------------------------
    # Sort
    # ----------------------------------------

    if result.empty:
        return result

    if sort_by == "Strike":

        result = result.sort_values(
            "strike"
        )

    elif sort_by == "Quantity":

        result = result.sort_values(
            "quantity",
            ascending=False,
        )

    elif sort_by == "Premium":

        result = result.sort_values(
            "sell_average",
            ascending=False,
        )

    elif sort_by == "Trade Date":

        result = result.sort_values(
            "trade_date",
            ascending=False,
        )

    elif sort_by == "Expiry":

        result = result.sort_values(
            "expiry_date"
        )

    return result