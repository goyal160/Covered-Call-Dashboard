import streamlit as st
import pandas as pd

from api import (
    get_cash_holdings,
    is_logged_in,
)

from services import cash_holding_summary

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

st.title("💰 Cash Holdings")

# =====================================================
# LOAD DATA
# =====================================================

cash = get_cash_holdings()

if cash is None:
    cash = pd.DataFrame()

summary = cash_holding_summary(cash)

# =====================================================
# KPI
# =====================================================

render_cash_summary(summary)

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

display_cash = cash.copy()

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

# =====================================================
# ADD FORM
# =====================================================

render_add_holding()

# =====================================================
# TABLE
# =====================================================

st.subheader("Current Holdings")

cash_holdings_table(display_cash)

st.divider()

# =====================================================
# CARDS
# =====================================================

render_holding_cards(display_cash)

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