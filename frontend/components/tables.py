import streamlit as st
import pandas as pd


# =====================================================
# GENERIC DATAFRAME
# =====================================================

def dataframe(
    df: pd.DataFrame,
    columns: list,
    rename: dict | None = None,
    hide_index: bool = True,
):
    """
    Generic dataframe renderer.

    Parameters
    ----------
    df : DataFrame

    columns : list
        Columns to display.

    rename : dict
        Optional column rename mapping.
    """

    if df.empty:

        st.info("No Records Found.")

        return

    display = df.copy()

    available = [
        c
        for c in columns
        if c in display.columns
    ]

    display = display[available]

    if rename:

        display.rename(
            columns=rename,
            inplace=True,
        )

    st.dataframe(

        display,

        hide_index=hide_index,

        width="stretch",

    )


# =====================================================
# CASH HOLDINGS TABLE
# =====================================================

def cash_holdings_table(df):

    if df.empty:

        st.info(
            "No Cash Holdings Available."
        )

        return

    display = df.copy()

    display["Investment"] = (

        display["buy_average"]

        *

        display["quantity"]

    )

    if "status" in display.columns:

        display["Current Value"] = display.apply(
            lambda r:
                r["close_price"] * r["quantity"]
                if r["status"] == "CLOSED"
                else r["current_price"] * r["quantity"],
            axis=1,
        )

        if "realized_gain" in display.columns:

            display["Gain/Loss"] = display.apply(
                lambda r:
                    r["realized_gain"]
                    if r["status"] == "CLOSED"
                    else r["gain_loss"],
                axis=1,
            )

        else:

            display["Gain/Loss"] = display["gain_loss"]

    else:

        display["Current Value"] = (
            display["current_price"]
            * display["quantity"]
        )

    name_col = (
        "holding_name"
        if "holding_name" in display.columns
        else "script_name"
    )

    dataframe(

        display,

        columns=[

            name_col,

            "status"

            "buy_average",

            "current_price",

            "quantity",

            "Investment",

            "Current Value",

            "gain_loss",

            "charges",

        ],

        rename={

            name_col: "Script",

            "status": "Status",

            "buy_average": "Buy Avg",

            "current_price": "Current Price",

            "quantity": "Qty",

            "Gain/Loss": "Gain/Loss",

            "charges": "Charges",

        },

    )


# =====================================================
# OPEN CALLS TABLE
# =====================================================

def open_calls_table(df):

    dataframe(

        df,

        columns=[

            "trade_date",

            "holding_name",

            "script_name",

            "strike",

            "sell_average",

            "quantity",

            "status",

        ],

        rename={

            "trade_date": "Trade Date",

            "holding_name": "Script",

            "script_name": "Script",

            "strike": "Strike",

            "sell_average": "Sell Avg",

            "quantity": "Qty",

            "status": "Status",

        },

    )


# =====================================================
# RECENT ACTIVITY TABLE
# =====================================================

def recent_activity_table(df):

    dataframe(

        df,

        columns=[

            "trade_date",

            "holding_name",

            "script_name",

            "strike",

            "sell_average",

            "quantity",

            "status",

        ],

        rename={

            "trade_date": "Trade Date",

            "holding_name": "Script",

            "script_name": "Script",

            "strike": "Strike",

            "sell_average": "Premium",

            "quantity": "Qty",

            "status": "Status",

        },

    )


# =====================================================
# CLOSED CALLS TABLE
# =====================================================

def closed_calls_table(df):

    dataframe(

        df,

        columns=[

            "trade_date",

            "holding_name",

            "script_name",

            "strike",

            "sell_average",

            "buy_average",

            "quantity",

            "net_profit",

            "close_date",

        ],

        rename={

            "trade_date": "Trade Date",

            "holding_name": "Script",

            "script_name": "Script",

            "strike": "Strike",

            "sell_average": "Sell Avg",

            "buy_average": "Buy Avg",

            "quantity": "Qty",

            "net_profit": "Net Profit",

            "close_date": "Close Date",

        },

    )