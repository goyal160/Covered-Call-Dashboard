import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar

from components.covered_calls.summary import render_summary
from components.covered_calls.add_form import render_add_form
from components.covered_calls.filters import filter_open_calls
from components.covered_calls.open_card import render_open_card
from components.covered_calls.closed_card import render_closed_card

from api import (
    get_open_calls,
    get_closed_calls,
    get_cash_holdings,
    is_logged_in,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Covered Calls",
    page_icon="📞",
    layout="wide",
)

# =====================================================
# AUTHENTICATION
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

st.title("📞 Covered Calls")

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=5)
def load_data(): 
    return (
        get_open_calls(),
        get_closed_calls(),
        get_cash_holdings(),
    )

open_df, closed_df, holdings = load_data()

st.write("Open DF")
st.dataframe(open_df)

st.write("Closed DF")
st.dataframe(closed_df)

# ============================================================
# ENSURE DATAFRAMES
# ============================================================

if open_df is None:
    open_df = pd.DataFrame()

if closed_df is None:
    closed_df = pd.DataFrame()

if holdings is None:
    holdings = pd.DataFrame()


# ============================================================
# CALCULATE KPI VALUES
# ============================================================

render_summary(
    open_df,
    closed_df,
)

st.divider()


# ============================================================
# ADD COVERED CALL
# ============================================================

render_add_form(
    holdings,
)

# ============================================================
# FILTER OPEN POSITIONS
# ============================================================

display_open = filter_open_calls(open_df)

# ============================================================
# TABS
# ============================================================

tab_open, tab_closed = st.tabs(
    [
        "🟢 Open Positions",
        "🔴 Closed Positions",
    ]
)

# ============================================================
# OPEN POSITIONS
# ============================================================

with tab_open:

    if display_open.empty:

        st.info("No Open Covered Call Positions.")

    else:

        st.subheader("Open Covered Calls")

        for _, row in display_open.iterrows():

            render_open_card(row)

# ============================================================
# CLOSED POSITIONS
# ============================================================

with tab_closed:

    if closed_df.empty:

        st.info("No Closed Positions.")

    else:

        st.subheader("Closed Covered Calls")

        for _, row in closed_df.iterrows():

            render_closed_card(row)