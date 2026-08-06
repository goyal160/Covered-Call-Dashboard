import streamlit as st
import pandas as pd

from api import (
    get_cash_holdings,
    is_logged_in,
    get_cash_transactions,
)

from components.cash.cash_transaction_form import render_cash_transaction_form
from services import cash_balance, cash_holding_summary

from components.sidebar import render_sidebar

from components.cash.summary import (
    render_cash_summary,
)

from components.cash.add_form import (
    render_add_holding,
)

from components.cash.holding_card import (
    render_holding_cards,
)

from components.cash.allocation_chart import (
    render_cash_allocation,
)

from components.cash.export_buttons import (
    render_export_buttons,
)

from components.tables import (
    cash_holdings_table,
)

from components.styles import load_css

load_css()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Cash Holdings",
    page_icon="💰",
    layout="wide",
)

# =====================================================
# LOGIN
# =====================================================

if not is_logged_in():

    st.warning(
        "Please login from Dashboard."
    )

    st.switch_page("Dashboard.py")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

render_sidebar(
    st.session_state["username"],
    show_dashboard=True,
)

# =====================================================
# TITLE
# =====================================================

st.title("💰 Cash Holdings & Portfolio Cash")

# =====================================================
# LOAD DATA
# =====================================================

cash = get_cash_holdings()

if cash is None:
    cash = pd.DataFrame()

if cash.empty:

    open_cash = pd.DataFrame()
    closed_cash = pd.DataFrame()

else:

    if "status" in cash.columns:

        open_cash = cash[
            cash["status"] == "OPEN"
        ]

        closed_cash = cash[
            cash["status"] == "CLOSED"
        ]

    else:

        open_cash = cash.copy()
        closed_cash = pd.DataFrame()

summary = cash_holding_summary(open_cash)

# =====================================================
# KPI
# =====================================================

render_cash_summary(summary)

transactions = get_cash_transactions()

if not transactions.empty:

    balance = pd.to_numeric(
        cash_balance()["cash_balance"],
        errors="coerce",
    )

    if pd.isna(balance):
        balance = 0

    st.info(
        f"💵 Available Cash Balance : ₹ {balance:,.2f}"
    )

st.divider()

# =====================================================
# SEARCH + SORT
# =====================================================

left, right = st.columns([3, 2])

search = left.text_input(
    "🔍 Search Script"
)

sort_by = right.selectbox(

    "Sort By",

    [

        "Script",

        "Investment",

        "Gain/Loss",

    ],

)

display_cash = open_cash.copy()

if not display_cash.empty:

    display_cash["Investment"] = (

        display_cash["buy_average"]

        *

        display_cash["quantity"]

    )

    if search:

        display_cash = display_cash[

            display_cash["script_name"]

            .str.contains(

                search,

                case=False,

                na=False,

            )

        ]

    if sort_by == "Script":

        display_cash = display_cash.sort_values(
            "script_name"
        )

    elif sort_by == "Investment":

        display_cash = display_cash.sort_values(

            "Investment",

            ascending=False,

        )

    else:

        display_cash = display_cash.sort_values(

            "gain_loss",

            ascending=False,

        )

# ============================================================
# CASH TRANSACTION
# ============================================================

render_cash_transaction_form()

st.divider()


# =====================================================
# ADD FORM
# =====================================================

render_add_holding()

# =====================================================
# OPEN / CLOSED HOLDINGS
# =====================================================

tab1, tab2 = st.tabs(
    [
        "📈 Open Holdings",
        "🔒 Closed Holdings",
    ]
)

# -----------------------------------------------------
# OPEN HOLDINGS
# -----------------------------------------------------

with tab1:

    st.subheader("Open Holdings")

    cash_holdings_table(display_cash)

    st.divider()

    render_holding_cards(display_cash)

# -----------------------------------------------------
# CLOSED HOLDINGS
# -----------------------------------------------------

with tab2:

    if closed_cash.empty:

        st.info("No closed holdings available.")

    else:

        closed_display = closed_cash.copy()


        numeric_cols = [
            "buy_average",
            "close_price",
            "quantity",
            "realized_gain",
            "charges",
        ]

        for col in numeric_cols:
            if col in closed_display.columns:
                closed_display[col] = pd.to_numeric(
                    closed_display[col],
                    errors="coerce",
                )


        closed_display["Investment"] = (
            closed_display["buy_average"]
            * closed_display["quantity"]
        )

        closed_display["Sale Value"] = (
            closed_display["close_price"]
            * closed_display["quantity"]
        )

        st.dataframe(
            closed_display[
                [
                    "script_name",
                    "close_date",
                    "Investment",
                    "Sale Value",
                    "realized_gain",
                ]
            ],
            hide_index=True,
            width="stretch",
        )

st.divider()

# =====================================================
# CHART
# =====================================================

render_cash_allocation(display_cash)

st.divider()

# =====================================================
# EXPORT
# =====================================================

if not display_cash.empty:

    export_df = display_cash.copy()

    export_df["Current Value"] = (

        export_df["current_price"]

        *

        export_df["quantity"]

    )

    export_df = export_df[

        [

            "script_name",

            "buy_average",

            "current_price",

            "quantity",

            "Investment",

            "Current Value",

            "gain_loss",

            "charges",

        ]

    ]

    export_df.columns = [

        "Script",

        "Buy Avg",

        "Current Price",

        "Qty",

        "Investment",

        "Current Value",

        "Gain/Loss",

        "Charges",

    ]

    render_export_buttons(export_df)

st.divider()