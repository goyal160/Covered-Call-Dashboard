from django.contrib.admin import display
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
        Data to display.

    columns : list
        Columns to display.

    rename : dict
        Optional column rename mapping.
    """

    if df is None or df.empty:

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

    if df is None or df.empty:

        st.info(
            "No Cash Holdings Available."
        )

        return

    display = df.copy()

    # -------------------------------------------------
    # Numeric conversion
    # -------------------------------------------------

    numeric_columns = [
        "buy_average",
        "current_price",
        "close_price",
        "quantity",
        "gain_loss",
        "realized_gain",
        "charges",
    ]

    for col in numeric_columns:

        if col in display.columns:

            display[col] = pd.to_numeric(
                display[col],
                errors="coerce",
            ).fillna(0)

    # -------------------------------------------------
    # Investment
    # -------------------------------------------------

    if {
        "buy_average",
        "quantity",
    }.issubset(display.columns):

        display["Investment"] = (
            display["buy_average"]
            *
            display["quantity"]
        )

    # -------------------------------------------------
    # Current Value
    # -------------------------------------------------

    if {
        "quantity",
        "status",
    }.issubset(display.columns):

        display["Current Value"] = display.apply(

            lambda r:
                r["close_price"] * r["quantity"]
                if str(r["status"]).upper() == "CLOSED"
                else r["current_price"] * r["quantity"],

            axis=1,

        )

    elif {
        "current_price",
        "quantity",
    }.issubset(display.columns):

        display["Current Value"] = (
            display["current_price"]
            *
            display["quantity"]
        )

    # -------------------------------------------------
    # Gain / Loss
    # -------------------------------------------------

    if "status" in display.columns:

        if "realized_gain" in display.columns:

            display["Gain/Loss"] = display.apply(

                lambda r:
                    r["realized_gain"]
                    if str(r["status"]).upper() == "CLOSED"
                    else r.get("gain_loss", 0),

                axis=1,

            )

        elif "gain_loss" in display.columns:

            display["Gain/Loss"] = (
                display["gain_loss"]
            )

    elif "gain_loss" in display.columns:

        display["Gain/Loss"] = (
            display["gain_loss"]
        )

    # -------------------------------------------------
    # Script name
    # -------------------------------------------------

    name_col = (

        "holding_name"
        if "holding_name" in display.columns
        else "script_name"

    )

    dataframe(

        display,

        columns=[

            name_col,

            "status",

            "buy_average",

            "current_price",

            "quantity",

            "Investment",

            "Current Value",

            "Gain/Loss",

            "charges",

        ],

        rename={

            name_col: "Script",

            "status": "Status",

            "buy_average": "Buy Avg",

            "current_price": "Current Price",

            "quantity": "Qty",

            "Investment": "Investment",

            "Current Value": "Current Value",

            "Gain/Loss": "Gain/Loss",

            "charges": "Charges",

        },

    )


# =====================================================
# DASHBOARD CASH HOLDINGS SUMMARY
# =====================================================

def cash_holding_summary_table(df):

    """
    Dashboard summary of cash holdings.

    Displays one row per cash holding:

        Sr. No.
        Script Name
        Status
        Realized Profit

    A total row is displayed at the bottom.

    Closed positions use realized_gain.
    Open positions have zero realized profit.
    """

    if df is None or df.empty:

        st.info(
            "No Cash Holdings Available."
        )

        return

    display = df.copy()

    # -------------------------------------------------
    # Numeric conversion
    # -------------------------------------------------

    if "realized_gain" in display.columns:

        display["realized_gain"] = pd.to_numeric(
            display["realized_gain"],
            errors="coerce",
        ).fillna(0)

    # -------------------------------------------------
    # Script name
    # -------------------------------------------------

    if "holding_name" in display.columns:

        display["Script Name"] = (
            display["holding_name"]
        )

    elif "script_name" in display.columns:

        display["Script Name"] = (
            display["script_name"]
        )

    else:

        display["Script Name"] = "Unknown"

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    if "status" in display.columns:

        display["Status"] = (
            display["status"]
            .astype(str)
            .str.upper()
        )

    else:

        display["Status"] = ""

    # -------------------------------------------------
    # Realized Profit
    # -------------------------------------------------

    if "realized_gain" in display.columns:

        display["Realized Profit"] = display.apply(

            lambda r:
                r["realized_gain"]
                if r["Status"] == "CLOSED"
                else 0.0,

            axis=1,

        )

    else:

        display["Realized Profit"] = 0.0

    # -------------------------------------------------
    # Build display table
    # -------------------------------------------------

    result = display[
        [
            "Script Name",
            "Status",
            "Realized Profit",
        ]
    ].copy()

    # -------------------------------------------------
    # Add Sr. No.
    # -------------------------------------------------

    result.insert(
        0,
        "Sr. No.",
        range(1, len(result) + 1),
    )

    # -------------------------------------------------
    # Total row
    # -------------------------------------------------

    total_profit = result[
        "Realized Profit"
    ].sum()

    total_row = pd.DataFrame(
        [
            {
                "Sr. No.": None,
                "Script Name": "Total",
                "Status": "",
                "Realized Profit": total_profit,
            }
        ]
    )

    result = pd.concat(
        [
            result,
            total_row,
        ],
        ignore_index=True,
    )

    # Keep Sr. No. Arrow-compatible while
    # allowing the Total row to remain blank.
    result["Sr. No."] = result[
        "Sr. No."
    ].astype("Int64")

    # -------------------------------------------------
    # Display
    # -------------------------------------------------

    st.dataframe(
        result,
        hide_index=True,
        width="stretch",
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

# =====================================================
# COVERED CALL SCRIPT-WISE SUMMARY
# =====================================================

def covered_call_summary_table(df):

    """
    Dashboard summary of covered calls grouped by script.

    Displays:

        Sr. No.
        Script Name
        Realized Profit from all calls sold pertaining to script
        Total Charges Incurred

    Only CLOSED calls contribute to realized profit.

    Charges include opening and closing charges
    for all calls belonging to the script.

    A final Total row displays the portfolio-wide
    realized profit and total charges.
    """

    if df is None or df.empty:

        st.info(
            "No Covered Call Records Available."
        )

        return

    display = df.copy()

    # -------------------------------------------------
    # Numeric conversion
    # -------------------------------------------------

    numeric_columns = [
        "net_profit",
        "opening_charges",
        "closing_charges",
    ]

    for col in numeric_columns:

        if col in display.columns:

            display[col] = pd.to_numeric(
                display[col],
                errors="coerce",
            ).fillna(0)

        else:

            display[col] = 0.0

    # -------------------------------------------------
    # Script name
    # -------------------------------------------------

    if "holding_name" in display.columns:

        display["Script Name"] = (
            display["holding_name"]
        )

    elif "script_name" in display.columns:

        display["Script Name"] = (
            display["script_name"]
        )

    else:

        display["Script Name"] = "Unknown"

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    if "status" in display.columns:

        display["Status"] = (
            display["status"]
            .astype(str)
            .str.upper()
        )

    else:

        display["Status"] = ""

    # -------------------------------------------------
    # Realized Profit
    # -------------------------------------------------

    # Only CLOSED calls contribute to realized profit.

    display["Realized Profit"] = 0.0

    closed_mask = (
        display["Status"] == "CLOSED"
    )

    display.loc[
        closed_mask,
        "Realized Profit"
    ] = display.loc[
        closed_mask,
        "net_profit"
    ]

    # -------------------------------------------------
    # Total Charges
    # -------------------------------------------------

    display["Total Charges"] = (
        display["opening_charges"]
        +
        display["closing_charges"]
    )

    # -------------------------------------------------
    # Group script-wise
    # -------------------------------------------------

    result = (

        display
        .groupby(
            "Script Name",
            sort=True,
            dropna=False,
        )
        .agg(
            {
                "Realized Profit": "sum",
                "Total Charges": "sum",
            }
        )
        .reset_index()

    )

    # -------------------------------------------------
    # Add Sr. No.
    # -------------------------------------------------

    result.insert(
        0,
        "Sr. No.",
        range(
            1,
            len(result) + 1,
        ),
    )

    # -------------------------------------------------
    # Add Total Row
    # -------------------------------------------------

    total_profit = result[
        "Realized Profit"
    ].sum()

    total_charges = result[
        "Total Charges"
    ].sum()

    total_row = pd.DataFrame(
        [
            {
                "Sr. No.": None,
                "Script Name": "Total",
                "Realized Profit": total_profit,
                "Total Charges": total_charges,
            }
        ]
    )

    result = pd.concat(
        [
            result,
            total_row,
        ],
        ignore_index=True,
    )

    # -------------------------------------------------
    # Display
    # -------------------------------------------------

    st.dataframe(
        result,
        hide_index=True,
        width="stretch",
    )

# =====================================================
# DIVIDEND SUMMARY
# =====================================================

def dividend_summary_table(dividend_df):

    columns = [
        "Sr. No.",
        "Script Name",
        "Dividend Date",
        "Dividend Income",
    ]    

    if dividend_df is None or dividend_df.empty:

        return pd.DataFrame(columns=columns)

    dividends = dividend_df.copy()

    # -------------------------------------------------
    # Numeric conversion
    # -------------------------------------------------

    if "amount" not in dividends.columns:

        dividends["amount"] = 0.0

    dividends["amount"] = pd.to_numeric(
        dividends["amount"],
        errors="coerce",
    ).fillna(0)

    # -------------------------------------------------
    # Script name
    # -------------------------------------------------

    if "holding_name" in dividends.columns:

        dividends["Script Name"] = (
            dividends["holding_name"]
        )

    elif "script_name" not in dividends.columns:

        dividends["Script Name"] = ""

    # -------------------------------------------------
    # Dividend date
    # -------------------------------------------------

    if "dividend_date" not in dividends.columns:

        dividends["dividend_date"] = ""

    # -------------------------------------------------
    # Create result
    # -------------------------------------------------

    result = dividends[
        [
            "script_name",
            "dividend_date",
            "amount",
        ]
    ].copy()

    result.rename(
        columns={
            "script_name": "Script Name",
            "dividend_date": "Dividend Date",
            "amount": "Dividend Income",
        },
        inplace=True,
    )

    # -------------------------------------------------
    # Sort latest dividend first
    # -------------------------------------------------

    result.sort_values(
        by="Dividend Date",
        ascending=False,
        inplace=True,
    )

    result.reset_index(
        drop=True,
        inplace=True,
    )

    # -------------------------------------------------
    # Serial number
    # -------------------------------------------------

    result.insert(
        0,
        "Sr. No.",
        range(1, len(result) + 1),
    )

    return result[
        [
            "Sr. No.",
            "Script Name",
            "Dividend Date",
            "Dividend Income",
        ]
    ]